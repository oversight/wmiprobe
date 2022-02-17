from .base import Base


class CheckWindowsPerfData(Base):

    qry = '''
    SELECT
    Name, C1TransitionsPersec, C2TransitionsPersec, C3TransitionsPersec,
    DPCRate, DPCsQueuedPersec, InterruptsPersec, PercentC1Time, PercentC2Time,
    PercentC3Time, PercentDPCTime, PercentIdleTime, PercentInterruptTime,
    PercentPrivilegedTime, PercentProcessorTime, PercentUserTime, Description
    FROM Win32_PerfFormattedData_PerfOS_Processor
    '''
    type_name = 'cpu'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Name'],
            'C1TransitionsPerSec': itm['C1TransitionsPersec'],
            'C2TransitionsPerSec': itm['C2TransitionsPersec'],
            'C3TransitionsPerSec': itm['C3TransitionsPersec'],
            'DPCRate': itm['DPCRate'],
            'DPCsQueuedPerSec': itm['DPCsQueuedPersec'],
            'InterruptsPerSec': itm['InterruptsPersec'],
            'PercentC1Time': itm['PercentC1Time'],
            'PercentC2Time': itm['PercentC2Time'],
            'PercentC3Time': itm['PercentC3Time'],
            'PercentDPCTime': itm['PercentDPCTime'],
            'PercentIdleTime': itm['PercentIdleTime'],
            'PercentInterruptTime': itm['PercentInterruptTime'],
            'PercentPrivilegedTime': itm['PercentPrivilegedTime'],
            'PercentProcessorTime': itm['PercentProcessorTime'],
            'PercentUserTime': itm['PercentUserTime'],
            'Description': itm['Description'],
        }
