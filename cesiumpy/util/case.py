import re
from typing import List, Pattern


def camel_case_to_snake_case(name: str) -> str:
    """
    Convert camelCase string to snake_case.
    """

    pattern_1: Pattern = re.compile(r"(.)([A-Z][a-z]+)")
    pattern_2: Pattern = re.compile(r"([a-z0-9])([A-Z])")

    name = pattern_1.sub(r"\1_\2", name)

    return pattern_2.sub(r"\1_\2", name).lower()


def snake_case_to_camel_case(name: str) -> str:
    """
    Convert snake_case string to camelCase.
    """

    parts: List[str] = name.split("_")

    return parts[0] + "".join(x.capitalize() if x else "_" for x in parts[1:])
