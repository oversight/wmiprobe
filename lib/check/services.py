from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..wmiquery import wmiquery
from ..utils import get_state


TYPE_NAME = "services"
QUERY = Query("""
    SELECT
    DesktopInteract, ExitCode, PathName, ServiceSpecificExitCode,
    ServiceType, State, Status, Name, DisplayName, Description, ProcessId,
    StartMode, StartName, Started
    FROM Win32_Service
""")


async def check_services(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows)
    return state
