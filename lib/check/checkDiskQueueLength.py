from .base import Base


class CheckDiskQueueLength(Base):

    qry = 'SELECT * FROM Win32_PerfFormattedData_PerfDisk_PhysicalDisk'
    type_name = 'disk'

    def on_item(self, itm):
        return {
            'name': itm['Name'],
            'avgDiskBytesPerRead': itm['AvgDiskBytesPerRead'],
            'avgDiskBytesPerTransfer': itm['AvgDiskBytesPerTransfer'],
            'avgDiskBytesPerWrite': itm['AvgDiskBytesPerWrite'],
            'avgDiskQueueLength': itm['AvgDiskQueueLength'],
            'avgDiskReadQueueLength': itm['AvgDiskReadQueueLength'],
            'avgDisksecPerRead': itm['AvgDisksecPerRead'],
            'avgDisksecPerTransfer': itm['AvgDisksecPerTransfer'],
            'avgDisksecPerWrite': itm['AvgDisksecPerWrite'],
            'avgDiskWriteQueueLength': itm['AvgDiskWriteQueueLength'],
            'durrentDiskQueueLength': itm['CurrentDiskQueueLength'],
            'description': itm['Description'],
            'diskBytesPerSec': itm['DiskBytesPersec'],
            'diskReadBytesPerSec': itm['DiskReadBytesPersec'],
            'diskReadsPerSec': itm['DiskReadsPersec'],
            'diskTransfersPerSec': itm['DiskTransfersPersec'],
            'diskWriteBytesPerSec': itm['DiskWriteBytesPersec'],
            'diskWritesPerSec': itm['DiskWritesPersec'],
            'frequency_Object': itm['Frequency_Object'],
            'frequency_PerfTime': itm['Frequency_PerfTime'],
            'frequency_Sys100NS': itm['Frequency_Sys100NS'],
            'percentDiskReadTime': itm['PercentDiskReadTime'],
            'percentDiskTime': itm['PercentDiskTime'],
            'percentDiskWriteTime': itm['PercentDiskWriteTime'],
            'percentIdleTime': itm['PercentIdleTime'],
            'splitIOPerSec': itm['SplitIOPerSec'],
            'timestamp_Object': itm['Timestamp_Object'],
            'timestamp_PerfTime': itm['Timestamp_PerfTime'],
            'timestamp_Sys100NS': itm['Timestamp_Sys100NS'],
        }
