from .base import Base


class CheckDiskIo(Base):

    qry = '''
    SELECT
    Name, DiskReadsPersec, DiskWritesPersec
    FROM Win32_PerfFormattedData_PerfDisk_LogicalDisk
    '''
    type_name = 'volume'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Name'],
            'readIOPS': itm['DiskReadsPersec'],
            'writeIOPS': itm['DiskWritesPersec'],
        }
