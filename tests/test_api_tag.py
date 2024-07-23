import pytest
from soundcld.api_handler import SoundCloud
from data_types import *

@pytest.fixture
def soundcloud_client():
    prompt = 'witch house'
    client = SoundCloud()
    return client, prompt

def test_get_track_by_tag(soundcloud_client):
    client, prompt = soundcloud_client
    all_tagged_tracks = client.get_track_by_tag(prompt)
    i = 0
    for track in all_tagged_tracks:
        if i > 20:
            break
        i += 1
        assert isinstance(track, BasicTrack)

if __name__ == '__main__':
    pytest.main()