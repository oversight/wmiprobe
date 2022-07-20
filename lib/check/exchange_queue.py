from aiowmi.query import Query
from libprobe.asset import Asset
from typing import Tuple
from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "exchange_queue"
QUERY = Query("""
    SELECT * FROM
    Win32_PerfFormattedData_MSExchangeTransportQueues_MSExchangeTransportQueues
""")


def on_item(itm: dict) -> dict:
    """Parse item.

    We lack information about the Win32_PerfFormattedData_MSExch.. class.
    It seems that at least exchange version 14.x is returning a single
    metric, for example `LargestDeliveryQueueLength` while (at least)
    version 15.x is returning two metrics for both Internal/External.
    Since no documentation can be found (at the time of writing) what the
    content of these metrics really are, we just test and merge them
    together to make the values compatible with earlier versions.

    Issue #4 (wmiprobe) is related.
    """

    a = itm.get('InternalAggregateDeliveryQueueLengthAllInternalQueues')
    b = itm.get('ExternalAggregateDeliveryQueueLengthAllExternalQueues')
    if a is not None and b is not None:
        itm['AggregateDeliveryQueueLengthAllQueues'] = a + b

    a = itm.get('InternalActiveRemoteDeliveryQueueLength')
    b = itm.get('ExternalActiveRemoteDeliveryQueueLength')
    if a is not None and b is not None:
        itm['ActiveRemoteDeliveryQueueLength'] = a + b

    a = itm.get('InternalRetryRemoteDeliveryQueueLength')
    b = itm.get('ExternalRetryRemoteDeliveryQueueLength')
    if a is not None and b is not None:
        itm['RetryRemoteDeliveryQueueLength'] = a + b

    a = itm.get('InternalLargestDeliveryQueueLength')
    b = itm.get('ExternalLargestDeliveryQueueLength')
    if a is not None and b is not None:
        itm['LargestDeliveryQueueLength'] = a + b

    itm['name'] = itm.pop('Name')
    return itm


async def check_exchange_queue(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    rows = await wmiquery(asset, asset_config, check_config, QUERY)
    state = get_state(TYPE_NAME, rows, on_item)
    return state
