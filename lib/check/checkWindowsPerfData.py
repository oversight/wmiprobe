from .base import Base


class CheckWindowsPerfData(Base):

    qry = '''
    SELECT
    Name, PercentProcessorTime
    FROM Win32_PerfFormattedData_PerfOS_Processor
    '''
    type_name = 'cpu'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Name'],
            'PercentProcessorTime': itm['PercentProcessorTime'],
        }
