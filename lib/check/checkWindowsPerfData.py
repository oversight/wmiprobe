from .base import Base


class CheckWindowsPerfData(Base):

    qry = 'SELECT * FROM Win32_PerfFormattedData_PerfOS_Processor'
    type_name = 'cpu'

    def on_item(self, itm):
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
            'Frequency_PerfTime': itm['Frequency_PerfTime'],
            'Frequency_Sys100NS': itm['Frequency_Sys100NS'],
            'Timestamp_Sys100NS': itm['Timestamp_Sys100NS'],
            'Description': itm['Description'],
            'Timestamp_PerfTime': itm['Timestamp_PerfTime'],
        }
