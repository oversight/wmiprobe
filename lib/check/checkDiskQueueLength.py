from .base import Base


class CheckDiskQueueLength(Base):

    qry = '''
    SELECT
    Name, AvgDiskQueueLength, AvgDiskReadQueueLength, AvgDiskWriteQueueLength,
    CurrentDiskQueueLength, DiskReadBytesPersec, DiskReadsPersec, 
    DiskWriteBytesPersec, DiskWritesPersec, PercentDiskReadTime,
    PercentDiskWriteTime
    FROM Win32_PerfFormattedData_PerfDisk_PhysicalDisk
    '''
    type_name = 'disk'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Name'],
            'avgDiskQueueLength': itm['AvgDiskQueueLength'],
            'avgDiskReadQueueLength': itm['AvgDiskReadQueueLength'],
            'avgDiskWriteQueueLength': itm['AvgDiskWriteQueueLength'],
            'currentDiskQueueLength': itm['CurrentDiskQueueLength'],
            'diskReadBytesPerSec': itm['DiskReadBytesPersec'],
            'diskReadsPerSec': itm['DiskReadsPersec'],
            'diskWriteBytesPerSec': itm['DiskWriteBytesPersec'],
            'diskWritesPerSec': itm['DiskWritesPersec'],
            'percentDiskReadTime': itm['PercentDiskReadTime'],
            'percentDiskWriteTime': itm['PercentDiskWriteTime'],
        }
