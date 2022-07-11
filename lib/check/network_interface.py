from aiowmi.query import Query
from libprobe.asset import Asset
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "interface"
QUERY = Query("""
    SELECT
    BytesReceivedPersec, BytesSentPersec, CurrentBandwidth, Name,
    PacketsOutboundDiscarded, PacketsOutboundErrors, PacketsReceivedDiscarded,
    PacketsReceivedErrors, OutputQueueLength
    FROM Win32_PerfFormattedData_Tcpip_NetworkInterface
""")


async def check_network_interface(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows)
    return state
