from .base import Base
from .valueLookups import CONFIG_MAN_ERR_CODE
from .valueLookups import AVAILABILITY_LU
from .valueLookups import STATUS_INFO
from .valueLookups import POW_MAN_CAP


class CheckPnpEntity(Base):

    qry = '''
    SELECT
    Availability, Caption, ClassGuid, CompatibleID, ConfigManagerErrorCode,
    ConfigManagerUserConfig, CreationClassName, Description, DeviceID,
    ErrorCleared, ErrorDescription, HardwareID, InstallDate, LastErrorCode,
    Manufacturer, PNPDeviceID, PowerManagementCapabilities,
    PowerManagementSupported, Service, Status, StatusInfo,
    SystemCreationClassName, SystemName
    FROM Win32_PnPEntity
    '''
    type_name = 'hardware'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['PNPDeviceID'],
            'availability': AVAILABILITY_LU.get(itm['Availability']),
            'caption': itm['Caption'],
            'classGuid': itm['ClassGuid'],
            'compatibleID': itm['CompatibleID'],
            'configManagerErrorCode':
                CONFIG_MAN_ERR_CODE.get(itm['ConfigManagerErrorCode']),
            'configManagerUserConfig': itm['ConfigManagerUserConfig'],
            'creationClassName': itm['CreationClassName'],
            'description': itm['Description'],
            'deviceID': itm['DeviceID'],
            'errorCleared': itm['ErrorCleared'],
            'errorDescription': itm['ErrorDescription'],
            'hardwareID': itm['HardwareID'],
            'installDate': itm['InstallDate'],
            'lastErrorCode': itm['LastErrorCode'],
            'manufacturer': itm['Manufacturer'],
            # 'pNPClass': itm['PNPClass'],
            'pNPDeviceID': itm['PNPDeviceID'],
            'powerManagementCapabilities':
                POW_MAN_CAP.get(itm['PowerManagementCapabilities']),
            'powerManagementSupported': itm['PowerManagementSupported'],
            # 'present': itm['Present'],
            'service': itm['Service'],
            'status': itm['Status'],
            'statusInfo': STATUS_INFO.get(itm['StatusInfo']),
            'systemCreationClassName': itm['SystemCreationClassName'],
            'systemName': itm['SystemName'],
        }
