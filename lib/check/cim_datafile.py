from genericpath import exists
import re

from aiowmi.query import Query
from libprobe.asset import Asset
from libprobe.exceptions import IgnoreCheckException
from typing import Tuple

from ..utils import get_state
from ..wmiquery import wmiquery


TYPE_NAME = "cim_datafile"


def on_item(itm: dict) -> Tuple[str, dict]:
    return {
        'fileSize': itm['FileSize'],  # int
        'hidden': itm['Hidden'],  # bool
        'lastAccessed': int(itm['LastAccessed']),  # time?
        'lastModified': int(itm['LastModified']),  # time?
        'readable': itm['Readable'],  # bool
        'system': itm['System'],  # bool
        'writeable': itm['Writeable'],  # bool
        'exists': True,  # bool
    }


async def check_cim_datafile(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    # TODO camelcase or snakecase
    cim_datafiles = check_config.get('cimDatafiles')
    if not cim_datafiles:
        raise IgnoreCheckException()

    select_from = (
        'SELECT Name, LastAccessed, LastModified, FileSize, Readable, '
        'Writeable, Hidden, System FROM cim_datafile'
    )

    # This sub will guarantee that the `file` string is created with 4
    # backslashes, in the `join` the 4 are escaped to 2, which are required
    # in the `Query`.
    files = (
        'name=\'' + re.sub(r"\\+", r"\\\\", fn) + '\''
        for fn in cim_datafiles)
    where_itms = ' OR '.join(files)
    qry = select_from + ' WHERE ' + where_itms

    rows = await wmiquery(asset, asset_config, check_config, Query(qry))
    state = get_state(TYPE_NAME, rows, on_item)
    type_state = state[TYPE_NAME]

    # Append non-existing files to the state
    for fn in cim_datafiles:
        if fn not in type_state:
            type_state[fn] = {'exists': False}

    return state
