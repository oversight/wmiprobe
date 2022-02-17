import asyncio
import datetime
import logging
from aiowmi.connection import Connection
from aiowmi.exceptions import WbemExInvalidClass
from aiowmi.exceptions import WbemExInvalidNamespace
from aiowmi.exceptions import WbemStopIteration, WbemException
from aiowmi.query import Query
from .utils import format_list


DTYPS_NOT_NULL = {
    int: 0,
    bool: False,
    float: 0.,
    list: '[]',
}


class Base:
    qry = None
    type_name = None
    interval = 300
    namespace = 'root/cimv2'
    required_services = []

    @classmethod
    async def run(cls, data, credentials=None):
        try:
            host_uuid = data['hostUuid']
            config = data['hostConfig']['probeConfig']['wmiProbe']
            ip4 = config['ip4']
            interval = data.get('checkConfig', {}).get('metaConfig', {}).get(
                'checkInterval')
            assert interval is None or isinstance(interval, int)
        except Exception:
            logging.error('invalid check configuration')
            return

        if credentials is None:
            logging.warning(f'missing credentials for {ip4}')
            return

        max_runtime = .8 * (interval or cls.interval)

        try:
            conn = Connection(ip4, **credentials)
            await conn.connect()
        except Exception:
            logging.error(f'unable to connect to {host_uuid} {ip4}')
            return

        try:
            service = await conn.negotiate_ntlm()
        except Exception:
            logging.error(f'unable to autheticate {host_uuid} {ip4}')

            conn.close()
            return

        max_runtime = .8 * (interval or cls.interval)
        try:
            state_data = await asyncio.wait_for(
                cls.get_data(conn, service),
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
            service.close()
            conn.close()

    @classmethod
    async def get_data(cls, conn, service):
        wmi_data = []
        try:
            query = Query(cls.qry, namespace=cls.namespace)
            await query.start(conn, service)

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
            state = cls.iterate_results(wmi_data)
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
    def iterate_results(cls, wmi_data):
        itms = cls.on_items(wmi_data)

        state = {}
        state[cls.type_name] = itms
        if '_Total' in itms:
            state[cls.type_name + '_Total'] = {
                '_Total': itms.pop('_Total')
            }
        return state
