from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery
from ..values import AVAILABILITY_LU, CONFIG_MAN_ERR_CODE, STATUS_INFO


TYPE_NAME = "hardware"
QUERY = Query("""
    SELECT
    Availability, ConfigManagerErrorCode, ConfigManagerUserConfig, Description,
    HardwareID, InstallDate, LastErrorCode, Manufacturer, PNPDeviceID,
    Service, Status, StatusInfo
    FROM Win32_PnPEntity
""")


def on_item(itm: dict) -> dict:
    itm['name'] = itm.pop('PNPDeviceID')
    return {
        **itm,
        'Availability': AVAILABILITY_LU.get(itm['Availability']),
        'ConfigManagerErrorCode':
            CONFIG_MAN_ERR_CODE.get(itm['ConfigManagerErrorCode']),
        'StatusInfo': STATUS_INFO.get(itm['StatusInfo']),
    }


async def check_pnp_entity(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
