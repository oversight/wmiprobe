from .base import Base
from .valueLookups import CONFIG_MAN_ERR_CODE
from .valueLookups import AVAILABILITY_LU
from .valueLookups import STATUS_INFO


class CheckPnpEntity(Base):

    qry = '''
    SELECT
    Availability, ConfigManagerErrorCode, ConfigManagerUserConfig, Description,
    HardwareID, InstallDate, LastErrorCode, Manufacturer, PNPDeviceID,
    Service, Status, StatusInfo
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
            'service': itm['Service'],
            'status': itm['Status'],
            'statusInfo': STATUS_INFO.get(itm['StatusInfo']),
        }
