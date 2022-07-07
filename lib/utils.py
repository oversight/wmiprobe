from typing import Callable, List, Tuple


def get_item(row: dict, name: str = 'Name') -> Tuple[str, dict]:
    """This is the default get item function. It requires at least that Name
    is a key in the row data."""
    return row.pop(name), row


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
        state[f"{type_name}Total"] = total

    return state
