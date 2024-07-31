"""
Stream And Repost Object
"""
import datetime
from dataclasses import dataclass
from typing import Optional

from soundcld.resource.base import BaseData
from soundcld.resource.playlist_album import BasicAlbumPlaylist
from soundcld.resource.track import BasicTrack
from soundcld.resource.user import BasicUser


@dataclass
class BaseStreamItem(BaseData):
    """
    Base Stream Object
    """
    created_at: datetime.datetime
    type: str
    user: BasicUser
    uuid: str
    caption: Optional[str]


@dataclass
class Reposted(BaseData):
    """
    Repost Object
    """
    target_urn: str
    user_urn: str
    caption: Optional[str]


@dataclass
class BaseStreamRepostItem(BaseStreamItem):
    """
    Base Reposted Stream Object
    """
    reposted: Optional[Reposted]


@dataclass
class TrackStreamItem(BaseStreamItem):
    """
    Track Post In User's Feed
    """
    track: BasicTrack


@dataclass
class TrackStreamRepostItem(BaseStreamRepostItem):
    """
    Track Repost In User's Feed
    """
    track: BasicTrack


@dataclass
class PlaylistStreamItem(BaseStreamItem):
    """
    Album Or Playlist Post In User's Feed
    """
    playlist: BasicAlbumPlaylist


@dataclass
class PlaylistStreamRepostItem(BaseStreamRepostItem):
    """
    Album Or Playlist Repost In User's Feed
    """
    playlist: BasicAlbumPlaylist
