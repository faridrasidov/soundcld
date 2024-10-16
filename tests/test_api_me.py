import pytest
from soundcld import SoundCloud
from soundcld.resource import (
    PlaylistStreamItem, TrackStreamItem,
    PlaylistStreamRepostItem, TrackStreamRepostItem,
    BasicTrack,
    User
)


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

def test_user_followers_followed_by_me(soundcloud_client):
    client = soundcloud_client
    followers_id = client.get_user_followers_followed_by_me(540941040)
    for follower in followers_id:
        print(follower)
        assert isinstance(follower, User)

def test_get_user_followings_not_followed_by_me(soundcloud_client):
    client = soundcloud_client
    following_id = client.get_user_followings_not_followed_by_me(540941040)
    for following in following_id:
        print(following)
        assert isinstance(following, User)

def test_get_my_streams(soundcloud_client):
    client = soundcloud_client
    streams = client.get_my_streams()
    for item in streams:
        print(item)
        assert isinstance(item, (PlaylistStreamItem,
                                 PlaylistStreamRepostItem,
                                 TrackStreamItem,
                                 TrackStreamRepostItem))

def test_get_my_reposts(soundcloud_client):
    client = soundcloud_client
    reposts = client.get_my_reposts()
    for item in reposts:
        print(item)
        assert isinstance(item, (PlaylistStreamRepostItem,
                                 TrackStreamRepostItem))

if __name__ == '__main__':
    pytest.main()