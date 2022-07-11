from aiowmi.query import Query
from libprobe.asset import Asset
from ..wmiquery import wmiquery
from ..utils import get_state


TYPE_NAME = "process"
QUERY = Query("""
    SELECT
    Name, CreatingProcessID, ElapsedTime, HandleCount, IDProcess,
    PageFaultsPersec, PageFileBytes, PageFileBytesPeak, PercentPrivilegedTime,
    PercentProcessorTime, PercentUserTime, PoolNonpagedBytes, PoolPagedBytes,
    PriorityBase, PrivateBytes, ThreadCount, VirtualBytes, VirtualBytesPeak,
    WorkingSet, WorkingSetPeak
    FROM Win32_PerfFormattedData_PerfProc_Process
""")

NON_SUMMABLES = {
    'Name',
    'CreatingProcessID',
    'IDProcess',
    'PageFileBytesPeak',
    'PriorityBase',
    'VirtualBytesPeak',
    'WorkingSetPeak',
}


async def check_process(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows)

    itms = state[TYPE_NAME]
    hash_names = [name for name in itms if '#' in name]
    for hash_name in hash_names:
        name = hash_name.split('#')[0]
        if name not in itms:
            continue
        hash_dct = itms.pop(hash_name)
        itm = itms[name]
        if 'ProcessCount' in itm:
            itm['ProcessCount'] += 1
        else:
            itm['ProcessCount'] = 2  # this is the second instance
        for ky in set(hash_dct) - NON_SUMMABLES:
            itm[ky] += hash_dct[ky]

    for itm in itms.values():
        itm['PrivateBytesAvg'] = \
            itm['PrivateBytes'] / itm.get('ProcessCount', 1)

    return state
