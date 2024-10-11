"""
Base Object For SoundCloud
"""
from dataclasses import dataclass, fields, is_dataclass
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
        """
        Return Value By Key
        """
        try:
            return getattr(self, item)
        except AttributeError:
            raise KeyError(f"Key '{item}' not found.")

    def __setitem__(self, item, value):
        """
        Set Value To Key
        """
        setattr(self, item, value)

    def items(self):
        """
        Return a generator of (field_name, value) tuples,
        converting dataclasses to dicts and datetime to ISO format.
        """
        return ((field.name, self._convert_to_dict(getattr(self, field.name))) for field in fields(self))

    def _convert_to_dict(self, value):
        """
        Helper method to convert nested
        dataclass objects to dictionaries recursively.
        Also handles datetime serialization (to ISO format).
        """
        if isinstance(value, datetime):
            return value.isoformat()
        elif is_dataclass(value):
            return {f.name: self._convert_to_dict(getattr(value, f.name)) for f in fields(value)}
        elif isinstance(value, (list, tuple)):
            return [self._convert_to_dict(v) for v in value]
        else:
            return value

    def __iter__(self):
        """
        Return an iterator over the field names.
        """
        return (field.name for field in fields(self))


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
