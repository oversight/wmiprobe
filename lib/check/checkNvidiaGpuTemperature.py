from .base import Base


THERMAL_LEVEL_LU = {
    '0': 'unknown',
    '1': 'normal',
    '2': 'warning',
    '3': 'critical',
}


class CheckNvidiaGpuTemperature(Base):

    qry = '''
    SELECT
    id, handle, temperature, thermalLevel, verClass, defaultMinTemperature,
    defaultMaxTemperature, type
    FROM ThermalProbe
    '''
    type_name = 'gpu'
    namespace = 'root/cimv2/nv'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['id'],
            'handle': itm['handle'],
            'temperature': itm['temperature'],
            'thermalLevel': THERMAL_LEVEL_LU.get(itm['thermalLevel'], '???'),
            'verClass': itm['verClass'],
            'defaultMaxTemperature': itm['defaultMaxTemperature'],
            'type': itm['type'],
            'defaultMinTemperature': itm['defaultMinTemperature'],
            'id': itm['id'],
        }
