from .base import Base


class CheckICAlatency(Base):

    qry = '''
    SELECT
    Name, LatencySessionAverage
    FROM Win32_PerfFormattedData_CitrixICA_ICASession
    '''
    type_name = 'ICAsession'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Name'].split('(')[-1][:-1],
            'latencySessionAverage': itm['LatencySessionAverage'],
        }
