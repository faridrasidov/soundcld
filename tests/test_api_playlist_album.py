import pytest
from soundcld import SoundCloud
from data_types import *

@pytest.fixture
def soundcloud_client():
    playlist_id = 1527297685
    client = SoundCloud()
    return client, playlist_id

def test_get_playlist(soundcloud_client):
    client, playlist_id = soundcloud_client
    playlist = client.get_playlist(playlist_id)
    print(playlist)
    assert isinstance(playlist, (AlbumPlaylist, BasicAlbumPlaylist))

def test_get_playlist_liker(soundcloud_client):
    client, playlist_id = soundcloud_client
    playlist_liker = client.get_playlist_liker(playlist_id)
    for user in playlist_liker:
        print(user)
        assert isinstance(user, (User, BasicUser))

def test_get_playlist_reposter(soundcloud_client):
    client, playlist_id = soundcloud_client
    playlist_reposter = client.get_playlist_reposter(playlist_id)
    for user in playlist_reposter:
        print(user)
        assert isinstance(user, (User, BasicUser))

if __name__ == '__main__':
    pytest.main()