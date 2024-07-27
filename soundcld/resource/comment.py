"""
Comment Object
"""
import datetime
from dataclasses import dataclass

from soundcld.resource.base import BaseData
from soundcld.resource.track import CommentTrack
from soundcld.resource.user import BasicUser


@dataclass
class CommentSelf(BaseData):
    """
    Comment Link
    """
    urn: str


@dataclass
class BasicComment(BaseData):
    """
    Comment Without Specified Track
    """
    kind: str
    id: int
    body: str
    created_at: datetime.datetime
    timestamp: int
    track_id: int
    user_id: int
    self: CommentSelf
    user: BasicUser


@dataclass
class Comment(BasicComment):
    """
    Comment With Specified Track
    """
    track: CommentTrack
