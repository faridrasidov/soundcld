"""
WebProfile Object
"""
from dataclasses import dataclass
from typing import Optional

from soundcld.resource.base import BaseData


@dataclass
class WebProfile(BaseData):
    """
    Web Profile Links Object
    """
    url: str
    network: str
    title: str
    username: Optional[str]
