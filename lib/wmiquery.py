import asyncio
import datetime
import logging
from aiowmi.query import Query
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


async def wmiquery(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        query: Query) -> List[Dict]:
    address = check_config.get('address')
    if not address:
        address = asset.name
    assert asset_config, 'missing credentials'
    username = asset_config['username']
    password = asset_config['password']
    if '\\' in username:
        # Replace double back-slash with single if required
        username = username.replace('\\\\', '\\')
        domain, username = username.split('\\')
    elif '@' in username:
        username, domain = username.split('@')
    else:
        domain = ''

    conn = Connection(address, username, password, domain)
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
            raise CheckException(f'unable to authenticate: {error_msg}')

        async with query.context(conn, service) as qc:
            async for props in qc.results():
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
    except CheckException:
        raise  # Re-raise check exceptions
    except Exception as e:
        error_msg = str(e) or type(e).__name__
        # At this point log the exception as this can be useful for debugging
        # issues with WMI queries;
        logging.exception(f'query error: {error_msg}; {asset}')
        raise CheckException(error_msg)
    finally:
        if service is not None:
            service.close()
        conn.close()

    return rows
