import datetime
import logging
from aiowmi.connection import Connection
from aiowmi.exceptions import WbemStopIteration, WbemException
from aiowmi.query import Query


DTYPS_NOT_NULL = {
    int,
    bool,
    float,
}


class Base:
    qry = None
    type_name = None
    interval = 300
    namespace = 'root/cimv2'
    required_services = []

    @classmethod
    async def get_data(cls, address, username, password):
        try:
            conn = Connection(address, username, password)
            await conn.connect()
            service = await conn.negotiate_ntlm()
            await conn.login_ntlm(service)
        except Exception:
            logging.exception('WMI connect error\n')
            raise

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
                        tp = prop.get_type()
                        row[name] = tp() if tp in DTYPS_NOT_NULL else None
                    elif isinstance(prop.value, datetime.datetime):
                        row[name] = int(prop.value.timestamp())  # TODOK int?
                    elif isinstance(prop.value, datetime.timedelta):
                        row[name] = int(prop.value.seconds)  # TODOK int?
                    elif isinstance(prop.value, list):
                        row[name] = ','.join(map(str, prop.value))  # TODOK
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
