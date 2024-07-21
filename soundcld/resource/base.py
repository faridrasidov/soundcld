"""
Base Object For SoundCloud
"""
from dacite import Config, from_dict
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
import dateutil.parser


@dataclass
class BaseData:
    dacite_config = Config(
        type_hooks={datetime: dateutil.parser.isoparse},
        cast=[tuple]
    )

    @classmethod
    def from_dict(cls, d: dict):
        return from_dict(cls, d, cls.dacite_config)

@dataclass
class BaseItem(BaseData):
    artwork_url: Optional[str]
    created_at: datetime
    description: Optional[str]
    display_date: datetime
    duration: int
    embeddable_by: str
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

    def get_all_tags(self) -> List[str]:
        tags = []
        if self.genre:
            tags.append(self.genre)
        return tags + [tag.strip() for tag in self.tag_list.split('"') if tag.strip()]