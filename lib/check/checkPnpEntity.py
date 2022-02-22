from .base import Base
from .valueLookups import CONFIG_MAN_ERR_CODE
from .valueLookups import AVAILABILITY_LU
from .valueLookups import STATUS_INFO
from .valueLookups import POW_MAN_CAP


class CheckPnpEntity(Base):

    qry = '''
    SELECT
    Availability, ConfigManagerErrorCode, ConfigManagerUserConfig, Description,
    HardwareID, InstallDate, LastErrorCode, Manufacturer, PNPDeviceID,
    PowerManagementCapabilities, PowerManagementSupported, Service, Status, 
    StatusInfo
    FROM Win32_PnPEntity
    '''
    type_name = 'hardware'

    @staticmethod
    def on_item(itm):

        return {
            'name': itm['PNPDeviceID'],
            'availability': AVAILABILITY_LU.get(itm['Availability']),
            'configManagerErrorCode':
                CONFIG_MAN_ERR_CODE.get(itm['ConfigManagerErrorCode']),
            'configManagerUserConfig': itm['ConfigManagerUserConfig'],
            'description': itm['Description'],
            'hardwareID': itm['HardwareID'],
            'installDate': itm['InstallDate'],
            'lastErrorCode': itm['LastErrorCode'],
            'manufacturer': itm['Manufacturer'],
            'powerManagementCapabilities':
                POW_MAN_CAP.get(itm['PowerManagementCapabilities']),
            'powerManagementSupported': itm['PowerManagementSupported'],
            'service': itm['Service'],
            'status': itm['Status'],
            'statusInfo': STATUS_INFO.get(itm['StatusInfo']),
        }
