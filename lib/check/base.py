import datetime
import logging
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
