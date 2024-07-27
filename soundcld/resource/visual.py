"""
Visual Object
"""
from typing import Tuple, Optional
from dataclasses import dataclass
from soundcld.resource.base import BaseData


@dataclass
class Visual(BaseData):
    """
    Visual Background Img Link
    """
    urn: str
    entry_time: int
    visual_url: str


@dataclass
class Visuals(BaseData):
    """
    Visual Background Img For Track,
    Playlist And Their User's Profile Visual.
    """
    urn: str
    enabled: bool
    tracking: Optional[str]
    visuals: Tuple[Visual]
