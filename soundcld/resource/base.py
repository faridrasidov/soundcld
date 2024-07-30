"""
Base Object For SoundCloud
"""
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from dacite import Config, from_dict
import dateutil.parser


@dataclass
class BaseData:
    """
    Base Data Object
    """
    dacite_config = Config(
        type_hooks={datetime: dateutil.parser.isoparse},
        cast=[tuple]
    )

    @classmethod
    def from_dict(cls, d: dict):
        """
        Converts Given Dict To Given Class Object
        """
        return from_dict(cls, d, cls.dacite_config)

@dataclass
class BaseItem(BaseData):
    """
    Base Item Is Common Datas
    """
    artwork_url: Optional[str]
    created_at: datetime
    description: Optional[str]
    display_date: datetime
    duration: int
    embeddable_by: Optional[str]
    genre: Optional[str]
    id: int
    kind: str
    label_name: Optional[str]
    last_modified: datetime
    licence: Optional[str]
    likes_count: Optional[int]
    permalink: str
    permalink_url: str
    public: bool
    release_date: Optional[str]
    reposts_count: Optional[int]
    secret_token: Optional[str]
    sharing: str
    tag_list: Optional[str]
    title: Optional[str]
    uri: str
    user_id: int
