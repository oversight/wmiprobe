from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery
from ..values import ACCESS_LU, CONFIG_MAN_ERR_CODE, DRIVE_TYPES


TYPE_NAME = "volume"
QUERY = Query("""
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
""")


def on_item(itm: dict) -> dict:
    free = itm['FreeSpace']
    total = itm['Capacity']
    used = total - free
    pct = 100. * used / total if total else 0.

    itm['name'] = itm.pop('Name')

    return {
        **itm,
        'Access': ACCESS_LU.get(itm['Access']),
        'ConfigManagerErrorCode':
            CONFIG_MAN_ERR_CODE.get(itm['ConfigManagerErrorCode']),
        'DriveType': DRIVE_TYPES.get(itm['DriveType']),
        'PercentUsed': pct,
    }


async def check_volume(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
