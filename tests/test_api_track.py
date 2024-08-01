import pytest
from soundcld import SoundCloud
from soundcld.resource import (
    BasicComment,
    AlbumPlaylist, BasicAlbumPlaylist,
    BasicTrack,
    User, BasicUser
)


@pytest.fixture
def soundcloud_client():
    track_id = 1727047206
    client = SoundCloud()
    return client, track_id

def test_get_track(soundcloud_client):
    client, track_id = soundcloud_client
    track = client.get_track(track_id)
    print(track)
    assert isinstance(track, BasicTrack)

def test_get_tracks(soundcloud_client):
    tracks_ids = [
        1703966532,
        1703966559,
        1703966610,
        1788589684,
        1788589690
    ]
    client, track_id = soundcloud_client
    tracks = client.get_tracks(tracks_ids)
    for track in tracks:
        print(track)
        assert isinstance(track, BasicTrack)

def test_get_track_liker(soundcloud_client):
    client, track_id = soundcloud_client
    track_liker = client.get_track_liker(track_id)
    for user in track_liker:
        print(user)
        assert isinstance(user, (User, BasicUser))

def test_get_track_reposter(soundcloud_client):
    client, track_id = soundcloud_client
    track_reposter = client.get_track_reposter(track_id)
    for user in track_reposter:
        print(user)
        assert isinstance(user, (User, BasicUser))

def test_get_albums_with_track(soundcloud_client):
    client, track_id = soundcloud_client
    track_added_albums = client.get_albums_with_track(track_id)
    for album in track_added_albums:
        print(album)
        assert isinstance(album, (AlbumPlaylist, BasicAlbumPlaylist))

def test_get_playlist_with_track(soundcloud_client):
    client, track_id = soundcloud_client
    track_added_playlists = client.get_playlists_with_track(track_id)
    for playlist in track_added_playlists:
        print(playlist)
        assert isinstance(playlist, (AlbumPlaylist, BasicAlbumPlaylist))

def test_get_track_comments(soundcloud_client):
    client, track_id = soundcloud_client
    comments = client.get_track_comments(track_id)
    for comment in comments:
        print(comment)
        assert isinstance(comment, BasicComment)

def test_get_related_tracks(soundcloud_client):
    client, track_id = soundcloud_client
    related_tracks = client.get_related_tracks(track_id)
    for track in related_tracks:
        print(track)
        assert isinstance(track, BasicTrack)

if __name__ == '__main__':
    pytest.main()