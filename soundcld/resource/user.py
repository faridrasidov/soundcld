"""
User Object
"""
from soundcld.resource.visual import Visuals
from soundcld.resource.base import BaseData
from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product(BaseData):
    id: str


@dataclass
class CreatorSubscription(BaseData):
    product: Product


@dataclass
class Badges(BaseData):
    pro: bool
    pro_unlimited: bool
    verified: bool


@dataclass
class BasicUser(BaseData):
    avatar_url: Optional[str]
    first_name: Optional[str]
    followers_count: Optional[int]
    full_name: Optional[str]
    id: int
    kind: str
    last_modified: datetime
    last_name: Optional[str]
    permalink: str
    permalink_url: str
    uri: str
    urn: str
    username: Optional[str]
    verified: bool
    city: Optional[str]
    country_code: Optional[str]
    badges: Badges
    station_urn: Optional[str]
    station_permalink: Optional[str]


@dataclass
class User(BasicUser):
    comments_count: Optional[int]
    created_at: datetime
    creator_subscriptions: Tuple[CreatorSubscription, ...]
    creator_subscription: CreatorSubscription
    description: Optional[str]
    followings_count: int
    groups_count: int
    likes_count: Optional[int]
    playlist_likes_count: Optional[int]
    playlist_count: int
    reposts_count: Optional[int]
    track_count: int
    visuals: Optional[Visuals]


@dataclass
class MissingUser(BaseData):
    id: int
    kind: str


@dataclass
class UserStatus(BaseData):
    status: str
    timestamp: str


@dataclass
class UserEmail(BaseData):
    address: str
    confirmed: bool
    id: int
    kind: str
    last_modified: datetime
    primary: bool
    urn: str
    user_id: str
