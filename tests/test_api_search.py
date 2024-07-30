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
        print(item)
        assert isinstance(item, (User, BasicUser,
                                 Track, BasicTrack,
                                 AlbumPlaylist, BasicAlbumPlaylist))

def test_get_search_tracks(soundcloud_client):
    client, prompt = soundcloud_client
    all_search_tracks = client.get_search_tracks(text=prompt)
    for item in all_search_tracks:
        print(item)
        assert isinstance(item, Track)

def test_get_search_users(soundcloud_client):
    client, prompt = soundcloud_client
    all_search_users = client.get_search_users(text=prompt)
    for item in all_search_users:
        print(item)
        assert isinstance(item, User)

def test_get_search_albums(soundcloud_client):
    client, prompt = soundcloud_client
    all_search_albums = client.get_search_albums(text=prompt)
    for item in all_search_albums:
        print(item)
        assert isinstance(item, AlbumPlaylist)

def test_get_search_playlists(soundcloud_client):
    client, prompt = soundcloud_client
    all_search_playlists = client.get_search_playlists(text=prompt)
    for item in all_search_playlists:
        print(item)
        assert isinstance(item, AlbumPlaylist)

if __name__ == '__main__':
    pytest.main()