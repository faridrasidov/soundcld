"""
Api Handler Of SoundCld
"""
import json
import os
import re
from dataclasses import dataclass
from typing import List, Union, Iterator
from datetime import datetime

import requests
from requests import HTTPError

from soundcld.resource.user import User
from soundcld.resource.track import BasicTrack
from soundcld.resource.message import Message
from soundcld.resource.conversation import Conversation
from soundcld.resource.playlist_album import BasicAlbumPlaylist
from soundcld.resource.comment import Comment, BasicComment
from soundcld.resource.webprofile import WebProfile
from soundcld.resource.alias import SearchItem, Like, RepostItem, StreamItem
from soundcld.request_handler import (GetReq, ListGetReq,
                                      CollectionGetReq)

scriptDirectory = os.path.dirname(os.path.abspath(__file__))
confDirectory = scriptDirectory + '/data.json'
cookieDirectory = scriptDirectory + '/cookies.json'
headerDirectory = scriptDirectory + '/headers.json'
infoDirectory = scriptDirectory + '/run_data.json'


@dataclass
class SoundCloud:
    """
    Main Soundcloud Class
    """
    auth: bool = False
    auto_id_gen: bool = False

    my_account_id: int = None
    cookies: dict = None
    headers: dict = None

    def __post_init__(self) -> None:
        self.data = {}
        oauth_key = ''
        self.__get_conf_last()
        if self.auth:
            self.__get_cookies()
            oauth_key = self.cookies['oauth_token']
        self.__get_headers(oauth_key=oauth_key)
        if not self.data['client_id']:
            self.generate_client_id()
        while not self.is_client_id_valid() and self.auto_id_gen:
            self.generate_client_id()
        self.__set_conf_last()

    def __get_conf_last(self) -> None:
        if os.path.exists(confDirectory):
            with open(confDirectory, 'r', encoding='utf-8') as file:
                config = json.load(file)
            self.data['user_id'] = config['user_id']
            self.data['client_id'] = config['client_id']
            self.data['app_version'] = config['app_version']
        else:
            dump_json = {
                'user_id': None,
                'client_id': None,
                'app_version': None
            }
            with open(confDirectory, 'w', encoding='utf-8') as file:
                json.dump(dump_json, file, indent=4)
            print('There Is No Data File')

    def __set_conf_last(self) -> None:
        config = {
            'user_id': self.data['user_id'],
            'client_id': self.data['client_id'],
            'app_version': self.data['app_version'],
        }
        with open(confDirectory, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)

    def __get_cookies(self) -> None:
        if os.path.exists(cookieDirectory):
            with open(cookieDirectory, 'r', encoding='utf-8') as file:
                self.cookies = json.load(file)
            if self.cookies['oauth_token']:
                temp = self.cookies['oauth_token'].split('-')
                self.my_account_id = temp[2]
        else:
            dump_json = {
                'moe_uuid': None,
                'oauth_token': None,
                'sc_anonymous_id': None
            }
            with open(cookieDirectory, 'w', encoding='utf-8') as file:
                json.dump(dump_json, file, indent=4)
            print('There Is No Data In Cookies File')

    def __get_headers(self, oauth_key: str) -> None:
        if os.path.exists(headerDirectory):
            to_add = ''
            if self.auth and oauth_key:
                elem = 'auth'
                to_add = f'OAuth {oauth_key}'
            else:
                elem = 'non_auth'
            with open(headerDirectory, 'r', encoding='utf-8') as file:
                self.headers = json.load(file)[elem]
            if self.auth:
                self.headers['Authorization'] = to_add
        else:
            print('There Is No Headers File')

    def __get_users(self, req: str, **param) -> Iterator[User]:
        return CollectionGetReq[User](self, req, User)(**param)

    def __get_tracks(self, req: str, **param) -> Iterator[BasicTrack]:
        return CollectionGetReq[BasicTrack](self, req, BasicTrack)(**param)

    def __get_album_playlist(self, req: str) -> Iterator[BasicAlbumPlaylist]:
        return CollectionGetReq[BasicAlbumPlaylist](self, req, BasicAlbumPlaylist)()

    def __get_likes(self, req: str, **param) -> Iterator[Like]:
        return CollectionGetReq[Like](self, req, Like)(**param)

    def __get_search(self, req: str, **param) -> Iterator[SearchItem]:
        param['user_id'] = self.data['user_id']
        return CollectionGetReq[SearchItem](self, req, SearchItem)(**param)

    def __get_id_list(self, req: str, **param) -> List:
        if self.is_logged_in():
            return ListGetReq[int](self, req, int)(**param)
        return ['Not Logged in']

    def __get_conversations(self, req: str, **param) -> Union[Iterator[Conversation], List[str]]:
        if self.is_logged_in():
            return CollectionGetReq[Conversation](self, req, Conversation)(**param)
        return ['Not Logged in']

    def __get_conversation_messages(self, req: str, **param) -> Union[Iterator[Message], List[str]]:
        if self.is_logged_in():
            return CollectionGetReq[Message](self, req, Message)(**param)
        return ['Not Logged in']

    def generate_client_id(self) -> None:
        """
        Gets Client ID, App Version And User ID
        """
        req = requests.get('https://soundcloud.com/', timeout=20)

        app_version = re.search(r'window\.__sc_version="\s*(\d+)"', req.text, re.DOTALL)
        user_id = re.search(r'window\.__sc_hydration\s*=\s*(\[\{.*?}]);', req.text, re.DOTALL)
        client_id = re.compile(r'client_id:\"([^\"]+)\"')
        asset_file = re.compile(r'src=\"(https:.{2}a-v2\.sndcdn\.com/assets/[^.]+\.js)\"')

        req.raise_for_status()
        matches = asset_file.findall(req.text)

        if app_version:
            app_version = app_version.group(1)
            self.data['app_version'] = app_version
        else:
            print('app_version not found')

        if user_id:
            user_id = user_id.group(1)
            user_id = json.loads(user_id)
            self.data['user_id'] = user_id[0]['data']
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
        self.data['client_id'] = client_id.group(1)

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

    def is_logged_in(self) -> bool:
        """
        Checks Do You Logged In Your Account
        {Do You Added Your Credentials To cookies.json}
        """
        if self.cookies:
            if all(self.cookies.values()):
                if os.path.exists(infoDirectory):
                    time_diff = self.__valid_time_diff()
                    if 0 < time_diff < 60:
                        self.__save_validate_time()
                        return True
                link = f'https://api-v2.soundcloud.com/users/{self.my_account_id}/conversations'
                param = {
                    'limit': 10,
                    'offset': 0,
                    'linked_partitioning': 1
                }
                req = requests.get(link, params=param,
                                   cookies=self.cookies,
                                   headers=self.headers,
                                   timeout=20)
                if req.status_code == 200:
                    self.__save_validate_time()
                    return True
        return False

    def get_user(self, user_id: int) -> User:
        """
        Get User By User ID
        """
        link = f'/users/{user_id}'
        return GetReq[User](self, link, User)()

    def get_user_tracks(self,
                        user_id: int,
                        representation: str = '',
                        limit: int = 20,
                        offset: int = 0,
                        linked_partitioning: int = 1):
        """
        Get User's Tracks By User ID
        """
        link = f'/users/{user_id}/tracks'
        param = {
            'representation': representation,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_tracks(link, **param)

    def get_user_top_tracks(self, user_id: int):
        """
        Get User's Top Tracks By User ID
        """
        link = f'/users/{user_id}/toptracks'
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

    def get_user_likes(self,
                       user_id: int,
                       limit: int = 10,
                       offset: int = 0,
                       linked_partitioning: int = 1):
        """
        Get User's Likes By User ID
        """
        link = f'/users/{user_id}/likes'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_likes(link, **param)

    def get_user_streams(self,
                         user_id: int,
                         limit: int = 24):
        """
        Get User's Streams/Reposts By User ID
        """
        link = f'/stream/users/{user_id}'
        param = {
            'offset': '',
            'limit': limit
        }
        return CollectionGetReq[StreamItem](self, link, StreamItem)(**param)

    def get_user_reposts(self,
                         user_id: int,
                         limit: int = 24):
        """
        Get User's Reposts By User ID
        """
        link = f'/stream/users/{user_id}/reposts'
        param = {
            'offset': '',
            'limit': limit
        }
        return CollectionGetReq[RepostItem](self, link, RepostItem)(**param)

    def get_user_comments(self,
                          user_id: int,
                          limit: int = 20,
                          offset: int = 0,
                          linked_partitioning: int = 1) -> Iterator[Comment]:
        """
        Get User's Comments By User ID
        """
        link = f'/users/{user_id}/comments'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return CollectionGetReq[Comment](self, link, Comment)(**param)

    def get_related_artists(self,
                            user_id: int,
                            creators_only: bool = False,
                            page_size: int = 12,
                            limit: int = 12,
                            offset: int = 0,
                            linked_partitioning: int = 1):
        """
        Get User Related Artists By User ID
        """
        link = f'/users/{user_id}/relatedartists'
        param = {
            'creators_only': creators_only,
            'page_size': page_size,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_users(link, **param)

    def get_user_followers(self,
                           user_id: int,
                           limit: int = 10,
                           offset: int = 0,
                           linked_partitioning: int = 1):
        """
        Get User's Follower Users By User ID
        """
        link = f'/users/{user_id}/followers'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_users(link, **param)

    def get_user_followings(self, user_id: int):
        """
        Get User's Following Users By User ID
        """
        link = f'/users/{user_id}/followings'
        return self.__get_users(link)

    def get_user_followings_not_followed_by_user(self,
                                                 user_id: int,
                                                 target_id: int,
                                                 limit: int = 3,
                                                 offset: int = 0,
                                                 linked_partitioning: int = 1):
        """
        Get User's Following Users, Which Not Followed By Target User
        """
        link = f'/users/{user_id}/followings/not_followed_by/{target_id}'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_users(link, **param)

    def get_user_followers_followed_by_user(self,
                                            user_id: int,
                                            target_id: int,
                                            limit: int = 10,
                                            offset: int = 0,
                                            linked_partitioning: int = 1):

        """
        Get User's Follower Users, Which Followed By Target User
        """
        link = f'/users/{user_id}/followers/followed_by/{target_id}'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_users(link, **param)

    def get_track(self, track_id: int) -> BasicTrack:
        """
        Get Track By Track ID
        """
        link = f'/tracks/{track_id}'
        return GetReq[BasicTrack](self, link, BasicTrack)()

    def get_tracks(self, track_ids: list[int]) -> List[BasicTrack]:
        """
        Get Multiple Tracks By Track IDs
        """
        link = '/tracks'
        param = {
            'ids': ','.join([str(its) for its in track_ids]),
            '%5Bobject%20Object%5D': ''
        }
        return ListGetReq[BasicTrack](self, link, BasicTrack)(**param)

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

    def get_track_comments(self,
                           track_id: int,
                           threaded: int = 1,
                           limit: int = 200,
                           offset: int = 0,
                           linked_partitioning: int = 1,
                           sort: str = 'newest') -> Iterator[BasicComment]:
        """
        Get Track Comments By Track ID
        """
        param = {
            'threaded': threaded,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning,
            'sort': sort,
        }
        link = f'/tracks/{track_id}/comments'
        return CollectionGetReq[BasicComment](self, link, BasicComment)(**param)

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

    def get_playlist(self, playlist_id: int) -> BasicAlbumPlaylist:
        """
        Get Playlist By Playlist ID
        """
        link = f'/playlists/{playlist_id}'
        return GetReq[BasicAlbumPlaylist](self, link, BasicAlbumPlaylist)()

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

    def get_albums_with_track(self, track_id: int):
        """
        Get Albums Where Track ID Have Been Added
        """
        link = f'/tracks/{track_id}/albums'
        return self.__get_album_playlist(link)

    def get_playlists_with_track(self, track_id: int):
        """
        Get Playlists Where Track ID Have Been Added
        """
        link = f'/tracks/{track_id}/playlists_without_albums'
        return self.__get_album_playlist(link)

    def get_search_all(self,
                       text: str,
                       facet: str = 'model',
                       variant_ids: str = '',
                       limit: int = 20,
                       offset: int = 0,
                       linked_partitioning: int = 1):
        """
        Get All Search Result {User, Track, Playlist}
        By Text To Search
        """
        link = '/search'
        param = {
            'q': text,
            'variant_ids': variant_ids,
            'facet': facet,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_search(link, **param)

    def get_search_tracks(self,
                          text: str,
                          facet: str = 'genre',
                          variant_ids: str = '',
                          limit: int = 20,
                          offset: int = 0,
                          linked_partitioning: int = 1):
        """
        Get All Search Tracks By Text To Search
        """
        link = '/search/tracks'
        param = {
            'q': text,
            'variant_ids': variant_ids,
            'facet': facet,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_search(link, **param)

    def get_search_users(self,
                         text: str,
                         facet: str = 'place',
                         variant_ids: str = '',
                         limit: int = 20,
                         offset: int = 0,
                         linked_partitioning: int = 1):
        """
        Get All Search Users By Text To Search
        """
        link = '/search/users'
        param = {
            'q': text,
            'variant_ids': variant_ids,
            'facet': facet,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_search(link, **param)

    def get_search_albums(self,
                          text: str,
                          facet: str = 'genre',
                          variant_ids: str = '',
                          limit: int = 20,
                          offset: int = 0,
                          linked_partitioning: int = 1):
        """
        Get All Search Albums By Text To Search
        """
        link = '/search/albums'
        param = {
            'q': text,
            'variant_ids': variant_ids,
            'facet': facet,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_search(link, **param)

    def get_search_playlists(self,
                             text: str,
                             facet: str = 'genre',
                             variant_ids: str = '',
                             limit: int = 20,
                             offset: int = 0,
                             linked_partitioning: int = 1):
        """
        Get All Search Playlists By Text To Search
        """
        link = '/search/playlists_without_albums'
        param = {
            'q': text,
            'variant_ids': variant_ids,
            'facet': facet,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_search(link, **param)

    def get_web_profiles(self, user_id: int) -> List[WebProfile]:
        """
        Get User's WebProfiles Users By User ID
        """
        if not user_id and self.is_logged_in():
            user_id = self.my_account_id
        link = f'/users/soundcloud:users:{user_id}/web-profiles'
        return ListGetReq[WebProfile](self, link, WebProfile)()

    def get_my_tracks(self):
        """
        Get My Tracks
        """
        return self.get_user_tracks(self.my_account_id, representation='owner')

    def get_user_followings_not_followed_by_me(self,
                                               user_id: int,
                                               limit: int = 3,
                                               offset: int = 0,
                                               linked_partitioning: int = 1):
        """
        Get User's Following Users, Which Not Followed By Me
        """
        link = f'/users/{user_id}/followings/not_followed_by/{self.my_account_id}'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_users(link, **param)

    def get_user_followers_followed_by_me(self,
                                          user_id: int,
                                          limit: int = 10,
                                          offset: int = 0,
                                          linked_partitioning: int = 1):

        """
        Get User's Follower Users, Which Followed By Me
        """
        link = f'/users/{user_id}/followers/followed_by/{self.my_account_id}'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_users(link, **param)

    def get_my_user_conversation(self,
                                 user_id: int,
                                 limit: int = 10,
                                 offset: int = 0,
                                 linked_partitioning: int = 1):
        """
        Get My Conversation Messages By User ID
        """
        link = f'/users/{self.my_account_id}/conversations/{user_id}/messages'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_conversation_messages(link, **param)

    def get_my_conversations_thumb(self,
                                   limit: int = 10,
                                   offset: int = 0,
                                   linked_partitioning: int = 1):
        """
        Get My Conversations Thumb {Last Message}
        """
        link = f'/users/{self.my_account_id}/conversations'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_conversations(link, **param)

    def get_my_unread_conversations(self,
                                    force: int = 1,
                                    limit: int = 20,
                                    offset: int = 0,
                                    linked_partitioning: int = 1):
        """
        Get My Unread Conversations
        """
        link = f'/users/{self.my_account_id}/conversations/unread'
        param = {
            'force': force,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_conversations(link, **param)

    def get_my_streams(self, limit: int = 24):
        """
        Get User's Streams/Reposts By User ID
        """
        link = f'/stream/users/{self.my_account_id}'
        param = {
            'offset': '',
            'limit': limit
        }
        return CollectionGetReq[StreamItem](self, link, StreamItem)(**param)

    def get_my_reposts(self, limit: int = 24):
        """
        Get User's Reposts By User ID
        """
        link = f'/stream/users/{self.my_account_id}/reposts'
        param = {
            'offset': '',
            'limit': limit
        }
        return CollectionGetReq[RepostItem](self, link, RepostItem)(**param)

    def get_my_liked_track_ids(self,
                               limit: int = 200):
        """
        Get My {Logged User} Liked Tracks IDs
        """
        link = '/me/track_likes/ids'
        param = {
            'offset': '',
            'limit': limit
        }
        return self.__get_id_list(link, **param)

    def get_my_track_reposts_ids(self,
                                 limit: int = 200):
        """
        Get My {Logged User} Track Reposts IDs
        """
        link = '/me/track_reposts/ids'
        param = {
            'limit': limit
        }
        return self.__get_id_list(link, **param)

    def get_my_liked_playlist_ids(self,
                                  limit: int = 5000,
                                  linked_partitioning: int = 1):
        """
        Get My {Logged User} Liked Playlist IDs
        """
        link = '/me/playlist_likes/ids'
        param = {
            'limit': limit,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_id_list(link, **param)

    def get_my_playlist_reposts_ids(self,
                                    limit: int = 200):
        """
        Get My {Logged User} Playlist Reposts IDs
        """
        link = '/me/playlist_reposts/ids'
        param = {
            'limit': limit
        }
        return self.__get_id_list(link, **param)

    def get_my_followers_ids(self,
                             limit: int = 5000,
                             linked_partitioning: int = 1):
        """
        Get My {Logged User} Followers IDs
        """
        link = '/me/followers/ids'
        param = {
            'limit': limit,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_id_list(link, **param)

    def get_my_following_ids(self,
                             limit: int = 5000,
                             linked_partitioning: int = 1):
        """
        Get My {Logged User} Followings IDs
        """
        link = f'/users/{self.my_account_id}/followings/ids'
        param = {
            'limit': limit,
            'linked_partitioning': linked_partitioning
        }
        return self.__get_id_list(link, **param)

    @staticmethod
    def __save_validate_time():
        json_dict = {
            'last_validate': datetime.now().isoformat()
        }
        with open(infoDirectory, 'w', encoding='utf-8') as file:
            json.dump(json_dict, file, indent=4)

    @staticmethod
    def __valid_time_diff() -> float:
        with open(infoDirectory, 'r', encoding='utf-8') as file:
            loaded_json = json.load(file)
            if 'last_validate' in loaded_json.keys():
                try:
                    saved_time = datetime.fromisoformat(loaded_json['last_validate'])
                except ValueError:
                    return -1
            else:
                return -1
        return (datetime.now() - saved_time).total_seconds()
