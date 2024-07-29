import pytest
from soundcld.api_handler import SoundCloud
from data_types import *

@pytest.fixture
def soundcloud_client():
    prompt = 'opium smoke'
    client = SoundCloud()
    return client, prompt

def test_get_search_all(soundcloud_client):
    client, prompt = soundcloud_client
    all_search = client.get_search_all(text=prompt)
    for item in all_search:
        assert isinstance(item, (User, BasicUser,
                                 Track, BasicTrack,
                                 AlbumPlaylist, BasicAlbumPlaylist))
        assert item.kind is not None

def test_get_search_tracks(soundcloud_client):
    client, prompt = soundcloud_client
    all_search_tracks = client.get_search_tracks(text=prompt)
    for item in all_search_tracks:
        assert isinstance(item, Track)
        assert item.kind is not None

def test_get_search_users(soundcloud_client):
    client, prompt = soundcloud_client
    all_search_users = client.get_search_users(text=prompt)
    for item in all_search_users:
        assert isinstance(item, User)
        assert item.kind is not None

def test_get_search_albums(soundcloud_client):
    client, prompt = soundcloud_client
    all_search_albums = client.get_search_albums(text=prompt)
    for item in all_search_albums:
        assert isinstance(item, AlbumPlaylist)
        assert item.kind is not None

def test_get_search_playlists(soundcloud_client):
    client, prompt = soundcloud_client
    all_search_playlists = client.get_search_playlists(text=prompt)
    for item in all_search_playlists:
        assert isinstance(item, AlbumPlaylist)
        assert item.kind is not None

if __name__ == '__main__':
    pytest.main()