from typing import Iterable


def pick_keys(d: dict, keys: Iterable[str]) -> dict:
    """
    Pick the given keys from the given dict
    """
    new_dict = {}
    for key in keys:
        if key in d:
            new_dict[key] = d[key]

    return new_dict
