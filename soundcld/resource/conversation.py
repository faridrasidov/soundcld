"""
Conversation Object
"""
import datetime
from dataclasses import dataclass
from typing import Tuple, Union

from soundcld.resource.base import BaseData
from soundcld.resource.message import Message
from soundcld.resource.user import BasicUser, MissingUser


@dataclass
class Conversation(BaseData):
    """
    Conversation Between Two Users
    """
    id: str
    last_message: Message
    read: bool
    started_at: datetime.datetime
    summary: str
    users: Tuple[Union[BasicUser, MissingUser], ...]