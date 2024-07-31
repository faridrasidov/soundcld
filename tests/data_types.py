"""
Test Data Types
"""
from soundcld.resource.user import User, BasicUser, MissingUser
from soundcld.resource.track import Track, BasicTrack, MiniTrack
from soundcld.resource.playlist_album import AlbumPlaylist, BasicAlbumPlaylist
from soundcld.resource.webprofile import WebProfile
from soundcld.resource.alias import SearchItem, Like
from soundcld.resource.comment import BasicComment, Comment
from soundcld.resource.message import Message
from soundcld.resource.conversation import Conversation
from soundcld.resource.like import TrackLike, PlaylistLike
from soundcld.resource.stream_repost import (
    PlaylistStreamItem,
    PlaylistStreamRepostItem,
    TrackStreamItem,
    TrackStreamRepostItem)