"""
Aliases For Common Objects
"""

from soundcld.resource.track import Track
from soundcld.resource.user import User
from soundcld.resource.playlist_album import AlbumPlaylist

from typing import Union


SearchItem = Union[Track, User, AlbumPlaylist]
