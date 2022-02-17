from .base import Base


class CheckUptime(Base):

    qry = '''
    SELECT
    SystemUpTime
    FROM Win32_PerfFormattedData_PerfOS_System
    '''
    type_name = 'uptime'

    @staticmethod
    def on_item(itm):
        return {
            'name': 'system',
            'uptime': itm['SystemUpTime']
        }
