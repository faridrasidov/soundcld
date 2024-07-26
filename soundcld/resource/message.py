"""
Message Object
"""
import datetime
from dataclasses import dataclass
from typing import Union

from soundcld.resource.base import BaseData
from soundcld.resource.user import BasicUser, MissingUser


@dataclass
class Message(BaseData):
    """
    Single Message Between Two Users
    """
    content: str
    conversation_id: str
    sender: Union[BasicUser, MissingUser]
    sender_urn: str
    sender_type: str
    sent_at: datetime.datetime
