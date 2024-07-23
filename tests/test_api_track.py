import pytest
from soundcld import SoundCloud
from data_types import *

@pytest.fixture
def soundcloud_client():
    track_id = 1727047206
    client = SoundCloud()
    return client, track_id

def test_get_track(soundcloud_client):
    client, track_id = soundcloud_client
    track = client.get_track(track_id)
    assert isinstance(track, BasicTrack)

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

def test_get_albums_with_track(soundcloud_client):
    client, track_id = soundcloud_client
    track_added_albums = client.get_albums_with_track(track_id)
    for album in track_added_albums:
        assert isinstance(album, (AlbumPlaylist, BasicAlbumPlaylist))

def test_get_playlist_with_track(soundcloud_client):
    client, track_id = soundcloud_client
    track_added_playlists = client.get_playlists_with_track(track_id)
    for playlist in track_added_playlists:
        assert isinstance(playlist, (AlbumPlaylist, BasicAlbumPlaylist))

def test_get_track_comments(soundcloud_client):
    client, track_id = soundcloud_client
    comments = client.get_track_comments(track_id)
    for comment in comments:
        assert isinstance(comment, BasicComment)

def test_get_related_tracks(soundcloud_client):
    client, track_id = soundcloud_client
    related_tracks = client.get_related_tracks(track_id)
    for track in related_tracks:
        assert isinstance(track, BasicTrack)

if __name__ == '__main__':
    pytest.main()
