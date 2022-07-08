import datetime
import time
from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "system"
QUERY = """
    SELECT
    Year, Month, Day, Hour, Minute, Second
    FROM Win32_UTCTime
"""


def on_item(itm: dict) -> Tuple[str, dict]:
    remote_ts = datetime.datetime(
        itm['Year'], itm['Month'], itm['Day'], itm['Hour'],
        itm['Minute'], itm['Second'],
        tzinfo=datetime.timezone.utc
    ).timestamp()
    ts = time.time()
    diff = abs(remote_ts - ts)
    # TODO proper item and metric names
    return 'system', {
        'timeDifference': diff
    }


async def check_system_time(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
