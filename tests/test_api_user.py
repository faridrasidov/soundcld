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

def test_get_user_streams(soundcloud_client):
    client, user_id = soundcloud_client
    streams = client.get_user_streams(user_id)
    for item in streams:
        print(item)
        assert isinstance(item, (PlaylistStreamItem,
                                 PlaylistStreamRepostItem,
                                 TrackStreamItem,
                                 TrackStreamRepostItem))

def test_get_user_reposts(soundcloud_client):
    client, user_id = soundcloud_client
    reposts = client.get_user_reposts(user_id)
    for item in reposts:
        print(item)
        assert isinstance(item, (PlaylistStreamRepostItem,
                                 TrackStreamRepostItem))

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

def test_get_user_followers_followed_by_user(soundcloud_client):
    client, user_id = soundcloud_client
    followers_id = client.get_user_followers_followed_by_user(540941040, user_id)
    for follower in followers_id:
        print(follower)
        assert isinstance(follower, User)

def test_get_user_followings_not_followed_by_user(soundcloud_client):
    client, user_id = soundcloud_client
    following_id = client.get_user_followings_not_followed_by_user(540941040, user_id)
    for following in following_id:
        print(following)
        assert isinstance(following, User)

def test_get_user_likes(soundcloud_client):
    client, user_id = soundcloud_client
    likes = client.get_user_likes(540941040)
    for like in likes:
        print(like)
        assert isinstance(like, (TrackLike, PlaylistLike))

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