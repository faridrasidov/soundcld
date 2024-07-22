import pytest
from soundcld import SoundCloud
from data_types import *

@pytest.fixture
def soundcloud_client():
    track_id = 1727047206
    client = SoundCloud()
    return client, track_id

def test_get_track_liker(soundcloud_client):
    client, track_id = soundcloud_client
    track_liker = client.get_track_liker(track_id)
    for user in track_liker:
        assert isinstance(user, (User, BasicUser))

def test_get_track_reposter(soundcloud_client):
    client, track_id = soundcloud_client
    track_reposter = client.get_track_reposter(track_id)
    for user in track_reposter:
        assert isinstance(user, (User, BasicUser))

if __name__ == '__main__':
    pytest.main()
