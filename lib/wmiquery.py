import asyncio
import datetime
import logging
from collections import defaultdict
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IgnoreCheckException
from aiowmi.query import Query
from aiowmi.connection import Connection
from aiowmi.exceptions import ServerNotOptimized, WbemStopIteration,\
    WbemExInvalidClass, WbemExInvalidNamespace
from typing import List, Dict


DTYPS_NOT_NULL = {
    int: 0,
    bool: False,
    float: 0.,
    list: [],
}


class Worker:
    def __init__(self):
        self.queue = asyncio.Queue(maxsize=30)  # at least the number of checks
        asyncio.ensure_future(self.worker())

    async def worker(self):
        while True:
            params, fut = await self.queue.get()
            try:
                res = await wmiquery_work(*params)
            except Exception as e:
                fut.set_exception(e)
            else:
                fut.set_result(res)
            finally:
                self.queue.task_done()


_workers = defaultdict(Worker)


def wmiquery(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        query_str: str,
        namespace: str = 'root/cimv2') -> List[Dict]:
    fut = asyncio.Future()

    worker = _workers[asset.id]
    logging.debug(f"Queue size for {asset.id} is {worker.queue.qsize()}")
    try:
        params = [asset, asset_config, check_config, query_str, namespace]
        worker.queue.put_nowait([params, fut])
    except asyncio.QueueFull:
        raise asyncio.QueueFull('Queue for this asset is full')
    return fut


async def wmiquery_work(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        query_str: str,
        namespace: str = 'root/cimv2') -> List[Dict]:
    query = Query(query_str, namespace=namespace)
    address = check_config.get('address')
    if not address:
        address = asset.name
    assert asset_config, 'missing credentials'

    conn = Connection(address, **asset_config)
    service = None
    rows = []

    try:
        await conn.connect()
    except Exception as e:
        error_msg = str(e) or type(e).__name__
        raise CheckException(f'unable to connect: {error_msg}')

    try:
        try:
            service = await conn.negotiate_ntlm()
        except Exception as e:
            error_msg = str(e) or type(e).__name__
            raise Exception(f'unable to authenticate: {error_msg}')

        await query.start(conn, service)

        try:
            await query.optimize()
        except ServerNotOptimized:
            logging.warning(f'server side is not optimized; {asset}')

        while True:
            try:
                res = await query.next()
            except WbemStopIteration:
                break

            props = res.get_properties()

            row = {}
            for name, prop in props.items():
                if prop.value is None:
                    row[name] = DTYPS_NOT_NULL.get(prop.get_type())
                elif isinstance(prop.value, datetime.datetime):
                    row[name] = prop.value.timestamp()
                elif isinstance(prop.value, datetime.timedelta):
                    row[name] = prop.value.seconds
                else:
                    row[name] = prop.value

            rows.append(row)
    except (WbemExInvalidClass, WbemExInvalidNamespace):
        raise IgnoreCheckException
    except Exception as e:
        error_msg = str(e) or type(e).__name__
        # At this point log the exception as this can be useful for debugging
        # issues with WMI queries;
        logging.exception(f'query error: {error_msg}; {asset}')
        raise CheckException(error_msg)
    finally:
        if service is not None:
            await query.done()
            service.close()
        conn.close()

    return rows
