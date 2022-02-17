from .base import Base


class CheckDiskQueueLength(Base):

    qry = '''
    SELECT
    Name, AvgDiskBytesPerRead, AvgDiskBytesPerTransfer, AvgDiskBytesPerWrite,
    AvgDiskQueueLength, AvgDiskReadQueueLength, AvgDisksecPerRead,
    AvgDisksecPerTransfer, AvgDisksecPerWrite, AvgDiskWriteQueueLength,
    CurrentDiskQueueLength, Description, DiskBytesPersec, DiskReadBytesPersec,
    DiskReadsPersec, DiskTransfersPersec, DiskWriteBytesPersec,
    DiskWritesPersec, PercentDiskReadTime, PercentDiskTime,
    PercentDiskWriteTime, PercentIdleTime, SplitIOPerSec
    FROM Win32_PerfFormattedData_PerfDisk_PhysicalDisk
    '''
    type_name = 'disk'

    @staticmethod
    def on_item(itm):
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
            'percentDiskReadTime': itm['PercentDiskReadTime'],
            'percentDiskTime': itm['PercentDiskTime'],
            'percentDiskWriteTime': itm['PercentDiskWriteTime'],
            'percentIdleTime': itm['PercentIdleTime'],
            'splitIOPerSec': itm['SplitIOPerSec'],
        }
