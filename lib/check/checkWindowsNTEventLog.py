from .base import Base


class CheckWindowsNTEventLog(Base):

    qry = '''
    SELECT
    FileName, FileSize, LogfileName, MaxFileSize, Name, NumberOfRecords, 
    OverWritePolicy, Status, Writeable, Sources
    FROM Win32_NTEventlogFile'''
    type_name = 'eventLog'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Name'],
            'fileName': itm['FileName'],
            'fileSize': itm['FileSize'],
            'logfileName': itm['LogfileName'],
            'maxFileSize': itm['MaxFileSize'],
            'numberOfRecords': itm['NumberOfRecords'],
            'overWritePolicy': itm['OverWritePolicy'],
            'sources': itm['Sources'],
            'status': itm['Status'],
            'writeable': itm['Writeable'],
        }
