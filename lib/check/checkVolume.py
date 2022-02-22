from .base import Base
from .valueLookups import ACCESS_LU
from .valueLookups import AVAILABILITY_LU
from .valueLookups import CONFIG_MAN_ERR_CODE
from .valueLookups import DRIVE_TYPES
from .valueLookups import STATUS_INFO


class CheckVolume(Base):

    qry = '''
    SELECT
    Name, Access, Automount, BlockSize, Capacity,
    Compressed, ConfigManagerErrorCode, ConfigManagerUserConfig,
    DeviceID, DirtyBitSet, DriveLetter,
    DriveType, ErrorCleared, ErrorDescription, ErrorMethodology, FileSystem,
    FreeSpace, IndexingEnabled, Label, LastErrorCode,
    MaximumFileNameLength, NumberOfBlocks,
    QuotasEnabled, QuotasIncomplete, QuotasRebuilding,
    SystemName, SerialNumber, SupportsDiskQuotas,
    SupportsFileBasedCompression
    FROM Win32_Volume
    '''
    type_name = 'volume'

    @staticmethod
    def on_item(itm):
        free = itm['FreeSpace']
        total = itm['Capacity']
        used = total - free
        pct = 100. * used / total if total else 0.

        return {
            'name': itm['Name'],
            'access': ACCESS_LU.get(itm['Access']),
            'automount': itm['Automount'],
            'blockSize': itm['BlockSize'],
            'capacity': total,
            'compressed': itm['Compressed'],
            'configManagerErrorCode':
                CONFIG_MAN_ERR_CODE.get(itm['ConfigManagerErrorCode']),
            'configManagerUserConfig': itm['ConfigManagerUserConfig'],
            'deviceID': itm['DeviceID'],
            'dirtyBitSet': itm['DirtyBitSet'],
            'driveLetter': itm['DriveLetter'],
            'driveType': DRIVE_TYPES.get(itm['DriveType']),
            'errorCleared': itm['ErrorCleared'],
            'errorDescription': itm['ErrorDescription'],
            'errorMethodology': itm['ErrorMethodology'],
            'fileSystem': itm['FileSystem'],
            'freeSpace': free,
            'indexingEnabled': itm['IndexingEnabled'],
            'label': itm['Label'],
            'lastErrorCode': itm['LastErrorCode'],
            'maximumFileNameLength': itm['MaximumFileNameLength'],
            'numberOfBlocks': itm['NumberOfBlocks'],
            'quotasEnabled': itm['QuotasEnabled'],
            'quotasIncomplete': itm['QuotasIncomplete'],
            'quotasRebuilding': itm['QuotasRebuilding'],
            # 'statusInfo': STATUS_INFO.get(itm['StatusInfo']),
            'systemName': itm['SystemName'],
            'serialNumber': itm['SerialNumber'],
            'supportsDiskQuotas': itm['SupportsDiskQuotas'],
            'supportsFileBasedCompression':
                itm['SupportsFileBasedCompression'],
            'percentUsed': pct
        }
