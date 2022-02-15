from .base import Base


class CheckICAlatency(Base):

    qry = 'SELECT Name, LatencySessionAverage FROM Win32_PerfFormattedData_CitrixICA_ICASession'
    type_name = 'ICAsession'
    required_services = ['wmi', 'citrix']

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['name'].split('(')[-1][:-1],
            'latencySessionAverage': itm['LatencySessionAverage'],
        }
