"""
Like Object
"""
import datetime
from dataclasses import dataclass

from soundcld.resource.base import BaseData
from soundcld.resource.playlist_album import AlbumPlaylistNoTracks
from soundcld.resource.track import BasicTrack


@dataclass
class BaseLike(BaseData):
    """
    Base Like Object
    """
    created_at: datetime.datetime
    kind: str


@dataclass
class TrackLike(BaseLike):
    """
    Track Like Object
    """
    track: BasicTrack


@dataclass
class PlaylistLike(BaseLike):
    """
    Playlist Like Object
    """
    playlist: AlbumPlaylistNoTracks
