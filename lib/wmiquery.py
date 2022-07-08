import datetime
import logging
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
    list: '[]',
}


async def wmiquery(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        query_str: str,
        namespace: str = 'root/cimv2') -> List[Dict]:
    query = Query(query_str, namespace=namespace)
    address = check_config['address']
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
                # TODOK elif isinstance(prop.value, list):
                #     row[name] = format_list(prop.value)
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
