from .base import Base


class CheckWindowsNTEventLog(Base):

    qry = '''
    SELECT
    FileName, Name, NumberOfRecords, Status
    FROM Win32_NTEventlogFile'''
    type_name = 'eventLog'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Name'],
            'fileName': itm['FileName'],
            'numberOfRecords': itm['NumberOfRecords'],
            'status': itm['Status'],
        }
