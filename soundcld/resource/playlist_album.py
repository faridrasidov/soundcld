"""
Album/Playlist Object For SoundCloud
"""
from soundcld.resource.track import BasicTrack, MiniTrack, Track, PublisherMetadata
from soundcld.resource.user import BasicUser, User
from soundcld.resource.base import BaseItem
from typing import Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseAlbumPlaylist(BaseItem):
    managed_by_feeds: bool
    set_type: str
    is_album: bool
    published_at: Optional[datetime]
    track_count: int
    tracks: Tuple[Union[Track, BasicTrack, MiniTrack], ...]


@dataclass
class AlbumPlaylist(BaseAlbumPlaylist):
    user: User


@dataclass
class BasicAlbumPlaylist(BaseAlbumPlaylist):
    user: BasicUser


@dataclass
class AlbumPlaylistNoTracks(BaseItem):
    managed_by_feeds: bool
    track_count: int
    set_type: str
    is_album: bool
    published_at: Optional[datetime]
    user: BasicUser
