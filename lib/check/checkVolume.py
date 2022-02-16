from .base import Base
from .valueLookups import ACCESS_LU
from .valueLookups import AVAILABILITY_LU
from .valueLookups import CONFIG_MAN_ERR_CODE
from .valueLookups import DRIVE_TYPES
from .valueLookups import POW_MAN_CAP
from .valueLookups import STATUS_INFO


class CheckVolume(Base):

    qry = '''
    SELECT
    Name, Access, Automount, Availability, BlockSize, Capacity, Caption,
    Compressed, ConfigManagerErrorCode, ConfigManagerUserConfig,
    CreationClassName, Description, DeviceID, DirtyBitSet, DriveLetter,
    DriveType, ErrorCleared, ErrorDescription, ErrorMethodology, FileSystem,
    FreeSpace, IndexingEnabled, InstallDate, Label, LastErrorCode,
    MaximumFileNameLength, NumberOfBlocks, PNPDeviceID,
    PowerManagementCapabilities, PowerManagementSupported, Purpose,
    QuotasEnabled, QuotasIncomplete, QuotasRebuilding, Status,
    SystemCreationClassName, SystemName, SerialNumber, SupportsDiskQuotas,
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
            'availability': AVAILABILITY_LU.get(itm['Availability']),
            'blockSize': itm['BlockSize'],
            'capacity': total,
            'caption': itm['Caption'],
            'compressed': itm['Compressed'],
            'configManagerErrorCode':
                CONFIG_MAN_ERR_CODE.get(itm['ConfigManagerErrorCode']),
            'configManagerUserConfig': itm['ConfigManagerUserConfig'],
            'creationClassName': itm['CreationClassName'],
            'description': itm['Description'],
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
            'installDate': itm['InstallDate'],
            'label': itm['Label'],
            'lastErrorCode': itm['LastErrorCode'],
            'maximumFileNameLength': itm['MaximumFileNameLength'],
            'numberOfBlocks': itm['NumberOfBlocks'],
            'pNPDeviceID': itm['PNPDeviceID'],
            'powerManagementCapabilities':
                POW_MAN_CAP.get(itm['PowerManagementCapabilities']),
            'powerManagementSupported': itm['PowerManagementSupported'],
            'purpose': itm['Purpose'],
            'quotasEnabled': itm['QuotasEnabled'],
            'quotasIncomplete': itm['QuotasIncomplete'],
            'quotasRebuilding': itm['QuotasRebuilding'],
            'status': itm['Status'],
            # 'statusInfo': STATUS_INFO.get(itm['StatusInfo']),
            'systemCreationClassName': itm['SystemCreationClassName'],
            'systemName': itm['SystemName'],
            'serialNumber': itm['SerialNumber'],
            'supportsDiskQuotas': itm['SupportsDiskQuotas'],
            'supportsFileBasedCompression':
                itm['SupportsFileBasedCompression'],
            'percentUsed': pct
        }
