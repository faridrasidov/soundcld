"""
WebProfiles Object
"""
from soundcld.resource.base import BaseData
from dataclasses import dataclass
from typing import Optional


@dataclass
class WebProfile(BaseData):
    url: str
    network: str
    title: str
    username: Optional[str]