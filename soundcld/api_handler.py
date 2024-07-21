"""
Api Handler Of SoundCld
"""
import configparser
import json
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Generator

import requests
from requests import HTTPError

from soundcld.data_types import *
from soundcld.request_handler import Requester, ListRequester, CollectionRequester, user_agent


@dataclass
class SoundCloud:
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    confDirectory = scriptDirectory + '/conf.cfg'
    authorization = None
    auth_token: str = None
    auto_id_gen: bool = False
    user_id: str = None
    client_id: str = None
    app_version: int = 0
    app_locale: str = 'en'
    user_agent: str = user_agent

    def __post_init__(self):
        if os.path.exists(self.confDirectory):
            self.__get_confLast()
        if not self.client_id:
            self.generate_clientId()
        while not self.is_client_id_valid():
            self.generate_clientId()
        self.set_confLast()

    def __get_confLast(self, ):
        config = configparser.ConfigParser()
        config.read(self.confDirectory)
        self.user_id = config['api']['user_id']
        self.client_id = config['api']['client_id']
        self.app_version = int(str(config['api']['app_version']))

    def set_confLast(self):
        config = configparser.ConfigParser()
        config['api'] = {
            'user_id': self.user_id,
            'client_id': self.client_id,
            'app_version': self.app_version,
        }
        with open(self.confDirectory, 'w') as cfg:
            config.write(cfg)

    def generate_clientId(self):
        req = requests.get("https://soundcloud.com/")

        appVersion = re.search(r'window\.__sc_version="\s*(\d+)"', req.text, re.DOTALL)
        userId = re.search(r'window\.__sc_hydration\s*=\s*(\[\{.*?}]);', req.text, re.DOTALL)
        clientId = re.compile(r"client_id:\"([^\"]+)\"")
        assetFile = re.compile(r"src=\"(https:.{2}a-v2\.sndcdn\.com/assets/[^.]+\.js)\"")

        req.raise_for_status()
        matches = assetFile.findall(req.text)

        if appVersion:
            appVersion = appVersion.group(1)
            self.app_version = appVersion
        else:
            print('app_version not found')

        if userId:
            userId = userId.group(1)
            userId = json.loads(userId)
            self.user_id = userId[0]['data']
        else:
            print('user_id not found')

        if not matches:
            return
        url = matches[-1]
        r = requests.get(url)
        r.raise_for_status()
        client_id = clientId.search(r.text)
        if not client_id:
            return
        self.client_id = client_id.group(1)

    def is_client_id_valid(self) -> bool:
        """
        Checks if current client_id is valid
        """
        try:
            self.get_searchTracks('GRXGVR')
            return True
        except HTTPError as err:
            if err.response.status_code == 401:
                return False
            else:
                raise

    def __get_users(self, req: str) -> Generator[User, None, None]:
        return CollectionRequester[User](self, req, User)()

    def __get_tracks(self, req: str) -> Generator[User, None, None]:
        return CollectionRequester[BasicTrack](self, req, BasicTrack)()

    def __get_albumPlaylist(self, req: str) -> Generator[User, None, None]:
        return CollectionRequester[BasicAlbumPlaylist](self, req, BasicAlbumPlaylist)()

    def __get_search(self, text: str, req: str, limit: int, offset: int) -> Generator[SearchItem, None, None]:
        param = {'q': f'{text}',
                 'user_id': self.user_id,
                 'limit': limit,
                 'offset': offset,
                 'linked_partitioning': 1,
                 }
        return CollectionRequester[SearchItem](self, req, SearchItem)(**param)

    def get_playlist(self, playlistId: int):
        link = f'/playlists/{playlistId}'
        return Requester[BasicAlbumPlaylist](self, link, BasicAlbumPlaylist)()

    def get_userTracks(self, userId: int):
        link = f'/users/{userId}/tracks'
        return self.__get_tracks(link)

    def get_userTopTracks(self, userId: int):
        link = f'/users/{userId}/toptracks'
        return self.__get_tracks(link)

    def get_userAlbums(self, userId: int):
        link = f'/users/{userId}/albums'
        return self.__get_albumPlaylist(link)

    def get_userPlaylists(self, userId: int):
        link = f'/users/{userId}/playlists_without_albums'
        return self.__get_albumPlaylist(link)

    def get_relatedArtists(self, userId: int):
        link = f'/users/{userId}/relatedartists'
        return self.__get_users(link)

    def get_userFollowers(self, userId: int):
        link = f'/users/{userId}/followers'
        return self.__get_users(link)

    def get_userFollowings(self, userId: int):
        link = f'/users/{userId}/followings'
        return self.__get_users(link)

    def get_trackLiker(self, trackId: int):
        link = f'/tracks/{trackId}/likers'
        return self.__get_users(link)

    def get_trackReposter(self, trackId: int):
        link = f'/tracks/{trackId}/reposters'
        return self.__get_users(link)

    def get_playlistLiker(self, playlistId: int):
        link = f'/playlists/{playlistId}/likers'
        return self.__get_users(link)

    def get_playlistReposter(self, playlistId: int):
        link = f'/playlists/{playlistId}/reposters'
        return self.__get_users(link)

    def get_searchAll(self, text, limit: int = 20, offset: int = 0):
        link = '/search'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_searchTracks(self, text, limit: int = 20, offset: int = 0):
        link = '/search/tracks'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_searchUsers(self, text, limit: int = 20, offset: int = 0):
        link = '/search/users'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_searchAlbums(self, text, limit: int = 20, offset: int = 0):
        link = '/search/albums'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_searchPlaylists(self, text, limit: int = 20, offset: int = 0):
        link = '/search/playlists_without_albums'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_webProfiles(self, userId: int = 0) -> List[WebProfile]:
        if not userId:
            userId = self.client_id
        link = f"/users/soundcloud:users:{userId}/web-profiles"
        return ListRequester[WebProfile](self, link, WebProfile)()

    def get_defaultHeader(self) -> Dict:
        return {"User-Agent": self.user_agent}