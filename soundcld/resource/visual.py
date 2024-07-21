"""
Visual Object (account background, music background)
"""
from soundcld.resource.base import BaseData
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class Visual(BaseData):
    urn: str
    entry_time: int
    visual_url: str


@dataclass
class Visuals(BaseData):
    urn: str
    enabled: bool
    tracking: Optional[str]
    visuals: Tuple[Visual]
