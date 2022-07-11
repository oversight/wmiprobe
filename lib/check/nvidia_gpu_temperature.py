from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = ""
QUERY = Query("""
    SELECT
    id, handle, temperature, thermalLevel, verClass, defaultMinTemperature,
    defaultMaxTemperature, type
    FROM ThermalProbe
""", namespace="root/cimv2/nv")

THERMAL_LEVEL_LU = {
    '0': 'unknown',
    '1': 'normal',
    '2': 'warning',
    '3': 'critical',
}


def on_item(itm: dict) -> Tuple[str, dict]:
    return itm.pop('id'), {
        **itm,
        'thermalLevel': THERMAL_LEVEL_LU.get(itm['thermalLevel']),
    }


async def check_nvidia_temperature(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
