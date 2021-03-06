import asyncio
import datetime
import logging
from collections import defaultdict
from agentcoreclient import IgnoreResultException
from aiowmi.connection import Connection
from aiowmi.exceptions import WbemExInvalidClass
from aiowmi.exceptions import WbemExInvalidNamespace
from aiowmi.exceptions import WbemStopIteration
from aiowmi.exceptions import WbemException
from aiowmi.exceptions import ServerNotOptimized
from aiowmi.query import Query
from .utils import format_list


DTYPS_NOT_NULL = {
    int: 0,
    bool: False,
    float: 0.,
    list: '[]',
}


class Worker:
    def __init__(self):
        self.queue = asyncio.Queue(maxsize=30)  # at least the number of checks
        asyncio.ensure_future(self.worker())

    async def worker(self):
        while True:
            cls, fut, data, asset_config = await self.queue.get()
            try:
                res = await cls._run(data, asset_config)
            except Exception as e:
                fut.set_exception(e)
            else:
                fut.set_result(res)
            finally:
                self.queue.task_done()


_workers = defaultdict(Worker)


class Base:
    qry = None
    type_name = None
    interval = 300
    namespace = 'root/cimv2'
    required = False

    @classmethod
    def run(cls, data, asset_config=None):
        fut = asyncio.Future()
        asset_id = data['hostUuid']

        worker = _workers[asset_id]
        logging.debug(f"Queue size for {asset_id} is {worker.queue.qsize()}")
        try:
            worker.queue.put_nowait([cls, fut, data, asset_config])
        except asyncio.QueueFull:
            raise asyncio.QueueFull('Queue for this asset is full')
        return fut

    @classmethod
    async def _run(cls, data, asset_config=None):
        try:
            asset_id = data['hostUuid']
            config = data['hostConfig']['probeConfig']['wmiProbe']
            ip4 = config['ip4']
            interval = data.get('checkConfig', {}).get('metaConfig', {}).get(
                'checkInterval')
            assert interval is None or isinstance(interval, int)
        except Exception as e:
            logging.error(f'invalid check configuration: `{e}`')
            raise Exception('Invalid check configuration')

        if asset_config is None or 'credentials' not in asset_config:
            logging.warning(f'missing asset config for {asset_id} {ip4}')
            raise Exception('Missing asset config')

        try:
            conn = Connection(ip4, **asset_config['credentials'])
            await conn.connect(timeout=10)
        except Exception as e:
            logging.error(
                f'unable to connect to {asset_id} {ip4}; '
                f'{e.__class__.__name__} {e}')
            raise Exception('Unable to connect')

        try:
            service = await conn.negotiate_ntlm()
        except Exception as e:
            logging.error(
                f'unable to authenticate {asset_id} {ip4}; '
                f'{e.__class__.__name__} {e}')
            conn.close()
            raise Exception('Unable to authenticate')

        max_runtime = .8 * (interval or cls.interval)
        query = cls._get_query(data)

        try:
            state_data = await asyncio.wait_for(
                cls.get_data(conn, service, query, data),
                timeout=max_runtime
            )
        except (WbemExInvalidClass, WbemExInvalidNamespace):
            # ignore invalid class and namespace errors
            # for citrix, exchange and nvidia checks
            pass
        except asyncio.TimeoutError:
            raise Exception('Check timed out.')
        except Exception as e:
            raise Exception(f'Check error: {e.__class__.__name__}: {e}')
        else:
            return state_data
        finally:
            await query.done()
            service.close()
            conn.close()

    @classmethod
    def _get_query(cls, data=None):
        return Query(cls.qry, namespace=cls.namespace)

    @classmethod
    async def get_data(cls, conn, service, query, data):
        wmi_data = []
        try:
            await query.start(conn, service)

            try:
                await query.optimize()
            except ServerNotOptimized:
                cinfo = conn.connection_info()
                logging.info(f'server side is not optimized ({cinfo})')

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
                    elif isinstance(prop.value, list):
                        row[name] = format_list(prop.value)
                    else:
                        row[name] = prop.value

                wmi_data.append(row)
        except WbemException:
            raise
        except Exception:
            logging.exception('WMI query error\n')
            raise

        try:
            state = cls.iterate_results(wmi_data, data)
        except Exception:
            logging.exception('WMI parse error\n')
            raise

        return state

    @classmethod
    def on_item(itm):
        return itm

    @classmethod
    def on_items(cls, itms):
        out = {}
        for i in itms:
            itm = cls.on_item(i)
            name = itm['name']
            out[name] = itm
        return out

    @classmethod
    def iterate_results(cls, wmi_data, data=None):
        itms = cls.on_items(wmi_data)

        state = {}
        state[cls.type_name] = itms
        if '_Total' in itms:
            state[cls.type_name + '_Total'] = {
                '_Total': itms.pop('_Total')
            }
        return state
