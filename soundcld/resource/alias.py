"""
Aliases For Common Objects
"""
from typing import Union
from soundcld.resource.track import Track, BasicTrack
from soundcld.resource.user import User, BasicUser
from soundcld.resource.playlist_album import AlbumPlaylist, BasicAlbumPlaylist
from soundcld.resource.like import TrackLike, PlaylistLike


SearchItem = Union[
    Track, BasicTrack,
    User, BasicUser,
    AlbumPlaylist, BasicAlbumPlaylist]

Like = Union[TrackLike, PlaylistLike]
