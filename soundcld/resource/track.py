"""
User Object
"""
from soundcld.resource.base import BaseData, BaseItem
from soundcld.resource.user import BasicUser, User
from soundcld.resource.visual import Visuals
from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Format(BaseData):
    protocol: str
    mime_type: str


@dataclass
class Transcoding(BaseData):
    url: str
    preset: str
    duration: int
    snipped: bool
    format: Format
    quality: str


@dataclass
class Media(BaseData):
    transcodings: Tuple[Transcoding, ...]


@dataclass
class PublisherMetadata(BaseData):
    id: str
    urn: str
    contains_music: bool


@dataclass
class BaseTrack(BaseItem):
    caption: Optional[str]
    comment_count: Optional[int]
    commentable: bool
    downloadable: bool
    download_count: Optional[int]
    full_duration: int
    has_downloads_left: bool
    media: Media
    monetization_model: str
    playback_count: Optional[int]
    policy: str
    purchase_title: Optional[str]
    purchase_url: Optional[str]
    state: str
    station_permalink: Optional[str]
    station_urn: Optional[str]
    streamable: bool
    track_authorization: str
    urn: str
    visuals: Optional[Visuals]
    waveform_url: str


@dataclass
class Track(BaseTrack):
    user: User


@dataclass
class BasicTrack(BaseTrack):
    user: BasicUser


@dataclass
class MiniTrack(BaseData):
    id: int
    kind: str
    monetization_model: str
    policy: str


@dataclass
class CommentTrack(BaseData):
    artwork_url: Optional[str]
    caption: Optional[str]
    id: int
    kind: str
    last_modified: datetime
    permalink: str
    permalink_url: str
    public: bool
    secret_token: Optional[str]
    sharing: str
    title: str
    uri: str
    urn: str
    user_id: int
    full_duration: int
    duration: int
    display_date: datetime
    media: Media
    station_urn: Optional[str]
    station_permalink: Optional[str]
    track_authorization: str
    monetization_model: str
    policy: str
    user: BasicUser