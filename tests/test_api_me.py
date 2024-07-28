import pytest
from soundcld.api_handler import SoundCloud

@pytest.fixture
def soundcloud_client():
    client = SoundCloud(auth=True)
    return client

def test_get_my_liked_track_ids(soundcloud_client):
    client = soundcloud_client
    track_ids = client.get_my_liked_track_ids()
    for track in track_ids:
        assert isinstance(track, int)

def test_get_my_reposts_ids(soundcloud_client):
    client = soundcloud_client
    repost_ids = client.get_my_reposts_ids()
    for repost in repost_ids:
        assert isinstance(repost, int)

def test_get_my_followers_ids(soundcloud_client):
    client = soundcloud_client
    followers_id = client.get_my_followers_ids()
    for follower in followers_id:
        assert isinstance(follower, int)

def test_get_my_following_ids(soundcloud_client):
    client = soundcloud_client
    following_id = client.get_my_following_ids()
    for following in following_id:
        assert isinstance(following, int)

if __name__ == '__main__':
    pytest.main()