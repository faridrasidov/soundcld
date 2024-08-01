"""
Aliases For Common Objects
"""
from typing import Union

from soundcld.resource.like import TrackLike, PlaylistLike
from soundcld.resource.playlist_album import AlbumPlaylist, BasicAlbumPlaylist
from soundcld.resource.stream_repost import (
    PlaylistStreamItem,
    PlaylistStreamRepostItem,
    TrackStreamItem,
    TrackStreamRepostItem,
)
from soundcld.resource.track import Track, BasicTrack
from soundcld.resource.user import User, BasicUser

SearchItem = Union[
    Track, BasicTrack,
    User, BasicUser,
    AlbumPlaylist, BasicAlbumPlaylist]

Like = Union[TrackLike, PlaylistLike]

RepostItem = Union[TrackStreamRepostItem, PlaylistStreamRepostItem]

StreamItem = Union[
    TrackStreamItem, TrackStreamRepostItem,
    PlaylistStreamItem, PlaylistStreamRepostItem]
