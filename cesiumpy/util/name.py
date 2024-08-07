# Apache License 2.0

from uuid import uuid4
from typing import Optional


def generate_name(prefix: Optional[str] = None) -> str:
    return f'{prefix or "property_"}{str(uuid4())[0:8]}'
