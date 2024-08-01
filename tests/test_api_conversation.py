import pytest
from soundcld import SoundCloud
from soundcld.resource import (
    Conversation,
    Message
)


@pytest.fixture
def soundcloud_client():
    user_id = 513663489
    client = SoundCloud(auth=True)
    return client, user_id

def test_get_my_conversations_thumb(soundcloud_client):
    client, user_id = soundcloud_client
    conversation_thumbs = client.get_my_conversations_thumb()
    for conversation in conversation_thumbs:
        print(conversation)
        assert isinstance(conversation, Conversation)

def test_get_my_unread_conversations(soundcloud_client):
    client, user_id = soundcloud_client
    conversation_unread = client.get_my_unread_conversations()
    for conversation in conversation_unread:
        print(conversation)
        assert isinstance(conversation, Conversation)

def test_get_my_user_conversation(soundcloud_client):
    client, user_id = soundcloud_client
    conversation_messages = client.get_my_user_conversation(user_id)
    for message in conversation_messages:
        print(message)
        assert isinstance(message, Message)

if __name__ == '__main__':
    pytest.main()