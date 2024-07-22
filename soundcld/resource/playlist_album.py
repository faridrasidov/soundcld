"""
Album/Playlist Object For SoundCloud
"""
from typing import Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
from soundcld.resource.base import BaseItem
from soundcld.resource.user import BasicUser, User
from soundcld.resource.track import BasicTrack, MiniTrack, Track


@dataclass
class BaseAlbumPlaylist(BaseItem):
    """
    Playlist/Album With Base Info
    """
    managed_by_feeds: bool
    set_type: str
    is_album: bool
    published_at: Optional[datetime]
    track_count: int
    tracks: Tuple[Union[Track, BasicTrack, MiniTrack], ...]


@dataclass
class AlbumPlaylist(BaseAlbumPlaylist):
    """
    Playlist/Album With Full User Info
    """
    user: User


@dataclass
class BasicAlbumPlaylist(BaseAlbumPlaylist):
    """
    Playlist/Album With Partial User Info
    """
    user: BasicUser


@dataclass
class AlbumPlaylistNoTracks(BaseItem):
    """
    Playlist/Album With No Track Info
    """
    managed_by_feeds: bool
    track_count: int
    set_type: str
    is_album: bool
    published_at: Optional[datetime]
    user: BasicUser
