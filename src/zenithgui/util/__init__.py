from .calc import _calculate_crc
from .path_utils import resource_path

__all__ = ["_calculate_crc", "resource_path"]

def get_fancy_name(name, dictionary: dict[str, str]):
    for key, value in dictionary.items():
        if name not in key:
            continue

        return value if (name in key) else name