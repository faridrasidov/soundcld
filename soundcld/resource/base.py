"""
Base Object For SoundCloud
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import dateutil.parser
from dacite import Config, from_dict


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

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            raise KeyError(f"Key '{item}' not found.")


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
