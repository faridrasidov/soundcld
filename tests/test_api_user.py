import pytest
from soundcld import SoundCloud
from data_types import *

@pytest.fixture
def soundcloud_client():
    user_id = 265222267
    client = SoundCloud()
    return client, user_id

def test_get_user(soundcloud_client):
    client, user_id = soundcloud_client
    user = client.get_user(user_id)
    print(user)
    assert isinstance(user, User)

def test_get_user_tracks(soundcloud_client):
    client, user_id = soundcloud_client
    user_tracks = client.get_user_tracks(user_id)
    for item in user_tracks:
        print(item)
        assert isinstance(item, (Track, BasicTrack))

def test_get_user_top_tracks(soundcloud_client):
    client, user_id = soundcloud_client
    user_top_tracks = client.get_user_top_tracks(user_id)
    for item in user_top_tracks:
        print(item)
        assert isinstance(item, (Track, BasicTrack))

def test_get_user_albums(soundcloud_client):
    client, user_id = soundcloud_client
    user_albums = client.get_user_albums(user_id)
    for item in user_albums:
        print(item)
        assert isinstance(item, (AlbumPlaylist, BasicAlbumPlaylist))

def test_get_user_playlists(soundcloud_client):
    client, user_id = soundcloud_client
    user_playlists = client.get_user_playlists(user_id)
    for item in user_playlists:
        print(item)
        assert isinstance(item, (AlbumPlaylist, BasicAlbumPlaylist))

def test_get_related_artists(soundcloud_client):
    client, user_id = soundcloud_client
    related_artists = client.get_related_artists(user_id)
    for user in related_artists:
        print(user)
        assert isinstance(user, (User, BasicUser))

def test_get_user_followers(soundcloud_client):
    client, user_id = soundcloud_client
    followers = client.get_user_followers(user_id)
    for user in followers:
        print(user)
        assert isinstance(user, (User, BasicUser))

def test_get_user_followings(soundcloud_client):
    client, user_id = soundcloud_client
    followings = client.get_user_followings(user_id)
    for user in followings:
        print(user)
        assert isinstance(user, (User, BasicUser))

def test_get_user_comments(soundcloud_client):
    client, user_id = soundcloud_client
    comments = client.get_user_comments(user_id)
    for comment in comments:
        print(comment)
        assert isinstance(comment, Comment)

def test_get_web_profiles(soundcloud_client):
    client, user_id = soundcloud_client
    comments = client.get_web_profiles(user_id)
    for comment in comments:
        print(comment)
        assert isinstance(comment, WebProfile)

if __name__ == '__main__':
    pytest.main()