from .base import Base


THERMAL_LEVEL_LU = {
    '0': 'unknown',
    '1': 'normal',
    '2': 'warning',
    '3': 'critical',
}


class CheckNvidiaGpuTemperature(Base):

    qry = 'SELECT id, handle, temperature, thermalLevel, verClass, defaultMinTemperature, defaultMaxTemperature, type  FROM ThermalProbe'
    type_name = 'gpu'
    namespace = 'root/cimv2/nv'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['id'],
            'handle': itm['handle'],  # "1",
            'temperature': itm['temperature'],  # "53",
            'thermalLevel': THERMAL_LEVEL_LU.get(itm['thermalLevel'], '???'),  # "1",
            'verClass': itm['verClass'],  # "Unsupported",
            'defaultMaxTemperature': itm['defaultMaxTemperature'],  # "127",
            'type': itm['type'],  # "1",
            'defaultMinTemperature': itm['defaultMinTemperature'],  # "-256",
            'id': itm['id'],  # "1"
        }
