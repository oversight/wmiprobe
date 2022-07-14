import datetime
from typing import Callable, List, Optional, Tuple, Union


def parse_wmi_date(val, fmt: Optional[str] = '%Y%m%d') -> Union[int, None]:
    if not val:
        return None
    try:
        val = int(datetime.datetime.strptime(val, fmt).timestamp())
        if val <= 0:
            return None
        return val
    except Exception:
        return None


def parse_wmi_date_1600(val) -> Union[int, None]:
    if not val:
        return None
    seconds1600 = 11644473600  # seconds from 1600
    try:
        val = int(val, 16) // 10000000 - seconds1600
        if val <= 0:
            return None
        return val
    except Exception:
        return None


def get_item(row: dict, name: str = 'Name') -> Tuple[str, dict]:
    """This is the default get item function. It requires at least that Name
    is a key in the row data."""
    return row.pop(name), row


def add_total_item(state: dict, total_item: dict, type_name: str):
    """Add a new Type to the state with a single item: `total`"""
    state[f"{type_name}Total"] = {'total': total_item}


def get_state(
        type_name: str,
        rows: List[dict],
        on_item: Callable[[dict], Tuple[str, dict]] = get_item) -> dict:
    """Default get_state function."""
    state = {
        type_name: dict((on_item(row) for row in rows))
    }

    # For some queries a Name='_Total' item exists. In this case we want to
    # create a new type ending with Total;
    total = state[type_name].pop('_Total', None)
    if total is not None:
        add_total_item(state, total, type_name)

    return state
