"""
Api Handler Of SoundCld
"""
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Union, Iterator

import requests
from requests import HTTPError

from soundcld.request_handler import (
    GetReq,
    ListGetReq,
    CollectionGetReq,
    PutReq,
    DeleteReq
)
from soundcld.resource import (
    SearchItem, Like, RepostItem, StreamItem,
    Comment, BasicComment,
    Conversation,
    Message,
    BasicAlbumPlaylist,
    BasicTrack,
    User,
    WebProfile
)

scriptDirectory = os.path.dirname(os.path.abspath(__file__))
confDirectory = scriptDirectory + '/data.json'
cookieDirectory = scriptDirectory + '/cookies.json'
headerDirectory = scriptDirectory + '/headers.json'
infoDirectory = scriptDirectory + '/run_data.json'


@dataclass
class BaseSound:
    """
    SoundCloud Core Class
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
            self.__get_conf_last()
            print('There Is No Data File')

    def __set_conf_last(self) -> None:
        config = {
            'user_id': self.data['user_id'],
            'client_id': self.data['client_id'],
            'app_version': self.data['app_version'],
        }
        with open(confDirectory, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)

    def _update_cookies(self):
        cookie = {
            'moe_uuid': self.cookies['moe_uuid'],
            'oauth_token': self.cookies['oauth_token'],
            'sc_anonymous_id': self.cookies['sc_anonymous_id'],
            'datadome': self.cookies['datadome']
        }
        with open(cookieDirectory, 'w', encoding='utf-8') as file:
            json.dump(cookie, file, indent=4)

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
            self.__get_cookies()
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

    def _get_user(self, req: str) -> User:
        return GetReq[User](self, req, User)()

    def _get_users(self, req: str, **param) -> Iterator[User]:
        return CollectionGetReq[User](self, req, User)(**param)

    def _get_track(self, req: str) -> BasicTrack:
        return GetReq[BasicTrack](self, req, BasicTrack)()

    def _get_track_list(self, req: str, **param) -> List[BasicTrack]:
        return ListGetReq[BasicTrack](self, req, BasicTrack)(**param)

    def _get_tracks(self, req: str, **param) -> Iterator[BasicTrack]:
        return CollectionGetReq[BasicTrack](self, req, BasicTrack)(**param)

    def _get_album_playlist(self, req: str) -> BasicAlbumPlaylist:
        return GetReq[BasicAlbumPlaylist](self, req, BasicAlbumPlaylist)()

    def _get_album_playlists(self, req: str) -> Iterator[BasicAlbumPlaylist]:
        return CollectionGetReq[BasicAlbumPlaylist](self, req, BasicAlbumPlaylist)()

    def _get_likes(self, req: str, **param) -> Iterator[Like]:
        return CollectionGetReq[Like](self, req, Like)(**param)

    def _get_searches(self, req: str, **param) -> Iterator[SearchItem]:
        param['user_id'] = self.data['user_id']
        return CollectionGetReq[SearchItem](self, req, SearchItem)(**param)

    def _get_reposts(self, req: str, **param) -> Iterator[StreamItem]:
        return CollectionGetReq[StreamItem](self, req, StreamItem)(**param)

    def _get_streams(self, req: str, **param) -> Iterator[RepostItem]:
        return CollectionGetReq[RepostItem](self, req, RepostItem)(**param)

    def _get_comments(self, req: str, **param) -> Iterator[Comment]:
        return CollectionGetReq[Comment](self, req, Comment)(**param)

    def _get_basic_comments(self, req: str, **param) -> Iterator[BasicComment]:
        return CollectionGetReq[BasicComment](self, req, BasicComment)(**param)

    def _get_id_list(self, req: str, **param) -> List:
        if self.is_logged_in():
            return ListGetReq[int](self, req, int)(**param)
        return ['Not Logged in']

    def _get_conversations(self, req: str, **param) -> Union[Iterator[Conversation], List[str]]:
        if self.is_logged_in():
            return CollectionGetReq[Conversation](self, req, Conversation)(**param)
        return ['Not Logged in']

    def _get_conversation_messages(self, req: str, **param) -> Union[Iterator[Message], List[str]]:
        if self.is_logged_in():
            return CollectionGetReq[Message](self, req, Message)(**param)
        return ['Not Logged in']

    def _get_web_profile_list(self, req: str) -> List[WebProfile]:
        return ListGetReq[WebProfile](self, req, WebProfile)()

    def _put_payload(self, req: str, **payload: dict) -> bool:
        if self.is_logged_in():
            return PutReq(self, req)(**payload)
        return False

    def _delete_payload(self, req: str, **payload: dict) -> bool:
        if self.is_logged_in():
            return DeleteReq(self, req)(**payload)
        return False

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
            link = '/tracks/1727047206'
            GetReq[BasicTrack](self, link, BasicTrack)()
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
