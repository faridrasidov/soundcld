import pytest
from soundcld.api_handler import SoundCloud
from data_types import *

@pytest.fixture
def soundcloud_client():
    client = SoundCloud(auth=True)
    return client

def test_get_my_tracks(soundcloud_client):
    client = soundcloud_client
    tracks = client.get_my_tracks()
    for track in tracks:
        print(track)
        assert isinstance(track, BasicTrack)

def test_get_my_liked_track_ids(soundcloud_client):
    client = soundcloud_client
    track_ids = client.get_my_liked_track_ids()
    for track in track_ids:
        print(track)
        assert isinstance(track, int)

def test_get_my_track_reposts_ids(soundcloud_client):
    client = soundcloud_client
    repost_ids = client.get_my_track_reposts_ids()
    for repost in repost_ids:
        print(repost)
        assert isinstance(repost, int)

def test_get_my_liked_playlist_ids(soundcloud_client):
    client = soundcloud_client
    playlist_ids = client.get_my_liked_playlist_ids()
    for playlist in playlist_ids:
        print(playlist)
        assert isinstance(playlist, int)

def test_get_my_playlist_reposts_ids(soundcloud_client):
    client = soundcloud_client
    repost_ids = client.get_my_playlist_reposts_ids()
    for repost in repost_ids:
        print(repost)
        assert isinstance(repost, int)

def test_get_my_followers_ids(soundcloud_client):
    client = soundcloud_client
    followers_id = client.get_my_followers_ids()
    for follower in followers_id:
        print(follower)
        assert isinstance(follower, int)

def test_get_my_following_ids(soundcloud_client):
    client = soundcloud_client
    following_id = client.get_my_following_ids()
    for following in following_id:
        print(following)
        assert isinstance(following, int)

if __name__ == '__main__':
    pytest.main()