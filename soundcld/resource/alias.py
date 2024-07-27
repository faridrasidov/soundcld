"""
Aliases For Common Objects
"""
from typing import Union
from soundcld.resource.track import Track, BasicTrack
from soundcld.resource.user import User, BasicUser
from soundcld.resource.playlist_album import AlbumPlaylist, BasicAlbumPlaylist



SearchItem = Union[
    Track, BasicTrack,
    User, BasicUser,
    AlbumPlaylist, BasicAlbumPlaylist]
