"""
Api Handler Of SoundCld
"""
import json
import os
import re
from dataclasses import dataclass
from typing import List, Generator

import requests
from requests import HTTPError

from soundcld.resource.user import User
from soundcld.resource.track import BasicTrack
from soundcld.resource.playlist_album import BasicAlbumPlaylist
from soundcld.resource.comments import Comment, BasicComment
from soundcld.resource.webprofiles import WebProfile
from soundcld.resource.aliases import SearchItem
from soundcld.request_handler import (Requester, ListRequester,
                                      CollectionRequester)


@dataclass
class SoundCloud:
    """
    Main Soundcloud Class
    """
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    confDirectory = scriptDirectory + '/data.json'
    authorization = None
    auth_token: str = None
    auto_id_gen: bool = False
    user_id: str = None
    client_id: str = None
    app_version: int = 0
    app_locale: str = 'en'

    def __post_init__(self):
        if os.path.exists(self.confDirectory):
            self.__get_conf_last()
        if not self.client_id:
            self.generate_client_id()
        while not self.is_client_id_valid():
            self.generate_client_id()
        self.__set_conf_last()

    def __get_conf_last(self, ):
        with open(self.confDirectory, 'r', encoding='utf-8') as file:
            config = json.load(file)
        self.user_id = config['user_id']
        self.client_id = config['client_id']
        self.app_version = config['app_version']

    def __set_conf_last(self):
        config = {
            'user_id': self.user_id,
            'client_id': self.client_id,
            'app_version': self.app_version,
        }
        with open(self.confDirectory, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)

    def __get_users(self, req: str) -> Generator[User, None, None]:
        return CollectionRequester[User](self, req, User)()

    def __get_tracks(self, req: str) -> Generator[User, None, None]:
        return CollectionRequester[BasicTrack](self, req, BasicTrack)()

    def __get_album_playlist(self, req: str) -> Generator[User, None, None]:
        return CollectionRequester[BasicAlbumPlaylist](self, req, BasicAlbumPlaylist)()

    def __get_search(self,
                     text: str,
                     req: str,
                     limit: int,
                     offset: int) -> Generator[SearchItem, None, None]:
        param = {'q': text,
                 'user_id': self.user_id,
                 'limit': limit,
                 'offset': offset,
                 'linked_partitioning': 1,
                 }
        return CollectionRequester[SearchItem](self, req, SearchItem)(**param)

    def generate_client_id(self):
        """
        Gets Client ID, App Version And User ID
        """
        req = requests.get("https://soundcloud.com/", timeout=20)

        app_version = re.search(r'window\.__sc_version="\s*(\d+)"', req.text, re.DOTALL)
        user_id = re.search(r'window\.__sc_hydration\s*=\s*(\[\{.*?}]);', req.text, re.DOTALL)
        client_id = re.compile(r"client_id:\"([^\"]+)\"")
        asset_file = re.compile(r"src=\"(https:.{2}a-v2\.sndcdn\.com/assets/[^.]+\.js)\"")

        req.raise_for_status()
        matches = asset_file.findall(req.text)

        if app_version:
            app_version = app_version.group(1)
            self.app_version = app_version
        else:
            print('app_version not found')

        if user_id:
            user_id = user_id.group(1)
            user_id = json.loads(user_id)
            self.user_id = user_id[0]['data']
        else:
            print('user_id not found')

        if not matches:
            return
        url = matches[-1]
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        client_id = client_id.search(r.text)
        if not client_id:
            return
        self.client_id = client_id.group(1)

    def is_client_id_valid(self) -> bool:
        """
        Checks Is Client ID valid
        """
        try:
            self.get_search_tracks('GRXGVR')
            return True
        except HTTPError as err:
            if err.response.status_code == 401:
                return False
            raise

    def get_playlist(self, playlist_id: int):
        """
        Get Playlist By Playlist ID
        """
        link = f'/playlists/{playlist_id}'
        return Requester[BasicAlbumPlaylist](self, link, BasicAlbumPlaylist)()

    def get_track(self, track_id: int):
        """
        Get Track By Track ID
        """
        link = f'/tracks/{track_id}'
        return Requester[BasicTrack](self, link, BasicTrack)()

    def get_track_comments(self, track_id: int, sort: str = 'newest', threaded: int = 1):
        """
        Get Track Comments By Track ID
        """
        param = {'sort': sort,
                 'threaded': threaded,
                 }
        link = f"/tracks/{track_id}/comments"
        return CollectionRequester[BasicComment](self, link, BasicComment)(**param)

    def get_user(self, user_id: int):
        """
        Get User By User ID
        """
        link = f'/users/{user_id}'
        return Requester[User](self, link, User)()

    def get_user_tracks(self, user_id: int):
        """
        Get User's Tracks By User ID
        """
        link = f'/users/{user_id}/tracks'
        return self.__get_tracks(link)

    def get_user_top_tracks(self, user_id: int):
        """
        Get User's Top Tracks By User ID
        """
        link = f'/users/{user_id}/toptracks'
        return self.__get_tracks(link)

    def get_user_comments(self, user_id: int):
        """
        Get User's Comments By User ID
        """
        link = f'/users/{user_id}/comments'
        return CollectionRequester[Comment](self, link, Comment)()

    def get_related_tracks(self, track_id: int):
        """
        Get Related Tracks By Track ID
        """
        link = f'/tracks/{track_id}/related'
        return self.__get_tracks(link)

    def get_track_by_tag(self, tag: str):
        """
        Get Recent Tracks With Tag Word
        """
        link = f'/recent-tracks/{tag}'
        return self.__get_tracks(link)

    def get_user_albums(self, user_id: int):
        """
        Get User's Albums By User ID
        """
        link = f'/users/{user_id}/albums'
        return self.__get_album_playlist(link)

    def get_user_playlists(self, user_id: int):
        """
        Get User's Playlists By User ID
        """
        link = f'/users/{user_id}/playlists_without_albums'
        return self.__get_album_playlist(link)

    def get_albums_with_track(self, track_id: int):
        """
        Get Albums Where Track ID Have Been Added
        """
        link = f'/tracks/{track_id}/albums"'
        return self.__get_album_playlist(link)

    def get_playlists_with_track(self, track_id: int):
        """
        Get Playlists Where Track ID Have Been Added
        """
        link = f'/tracks/{track_id}/playlists_without_albums"'
        return self.__get_album_playlist(link)

    def get_related_artists(self, user_id: int):
        """
        Get User Related Artists By User ID
        """
        link = f'/users/{user_id}/relatedartists'
        return self.__get_users(link)

    def get_user_followers(self, user_id: int):
        """
        Get User's Follower Users By User ID
        """
        link = f'/users/{user_id}/followers'
        return self.__get_users(link)

    def get_user_followings(self, user_id: int):
        """
        Get User's Following Users By User ID
        """
        link = f'/users/{user_id}/followings'
        return self.__get_users(link)

    def get_track_liker(self, track_id: int):
        """
        Get Track's Liker Users By Track ID
        """
        link = f'/tracks/{track_id}/likers'
        return self.__get_users(link)

    def get_track_reposter(self, track_id: int):
        """
        Get Track's Reposter Users By Track ID
        """
        link = f'/tracks/{track_id}/reposters'
        return self.__get_users(link)

    def get_playlist_liker(self, playlist_id: int):
        """
        Get Playlist's Liker Users By Playlist ID
        """
        link = f'/playlists/{playlist_id}/likers'
        return self.__get_users(link)

    def get_playlist_reposter(self, playlist_id: int):
        """
        Get Playlist's Reposter Users By Playlist ID
        """
        link = f'/playlists/{playlist_id}/reposters'
        return self.__get_users(link)

    def get_search_all(self, text, limit: int = 20, offset: int = 0):
        """
        Get All Search Result {User, Track, Playlist}
        By Text To Search
        """
        link = '/search'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_search_tracks(self, text, limit: int = 20, offset: int = 0):
        """
        Get All Search Tracks By Text To Search
        """
        link = '/search/tracks'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_search_users(self, text, limit: int = 20, offset: int = 0):
        """
        Get All Search Users By Text To Search
        """
        link = '/search/users'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_search_albums(self, text, limit: int = 20, offset: int = 0):
        """
        Get All Search Albums By Text To Search
        """
        link = '/search/albums'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_search_playlists(self, text, limit: int = 20, offset: int = 0):
        """
        Get All Search Playlists By Text To Search
        """
        link = '/search/playlists_without_albums'
        return self.__get_search(text=text, req=link, limit=limit, offset=offset)

    def get_web_profiles(self, user_id: int = 0) -> List[WebProfile]:
        """
        Get User's WebProfiles Users By User ID
        """
        if not user_id:
            user_id = self.client_id
        link = f"/users/soundcloud:users:{user_id}/web-profiles"
        return ListRequester[WebProfile](self, link, WebProfile)()
