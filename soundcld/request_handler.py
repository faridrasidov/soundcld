"""
Request Handler Of SoundCld
"""
from dataclasses import dataclass
from typing import Optional, Dict, Generic, TypeVar, get_origin, Union, List

import string
import requests
from dacite import MissingValueError

from soundcld.resource.user import User, BasicUser
from soundcld.resource.track import Track, BasicTrack
from soundcld.resource.playlist_album import AlbumPlaylist, BasicAlbumPlaylist

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
T = TypeVar('T')


def _convert_dict(data, return_type: T):
    union = get_origin(return_type) is Union
    data_type = ''
    union_types = {
        'user': [User, BasicUser],
        'track':[Track, BasicTrack],
        'playlist':[AlbumPlaylist, BasicAlbumPlaylist]
    }
    if union:
        if 'kind' in data.keys():
            data_type = data['kind']
        if data_type in union_types:
            for t in union_types[data_type]:
                try:
                    return t.from_dict(data)
                except MissingValueError as err:
                    print(err)
    else:
        return return_type.from_dict(data)
    raise ValueError(f"Could not convert {data} to type {return_type}")


@dataclass
class Requester(Generic[T]):
    """
    Core Class To Send Request To Soundcloud
    """
    base = "https://api-v2.soundcloud.com"
    resource_url = params = headers = ''
    client: T
    format_url: str
    return_type: T

    def _format_url_and_remove_params(self, kwargs: dict) -> str:
        format_args = {tup[1]
                       for tup in string.Formatter().parse(self.format_url)
                       if tup[1] is not None}
        args = {}
        for k in list(kwargs.keys()):
            if k in format_args:
                args[k] = kwargs.pop(k)
        return self.base + self.format_url.format(**args)

    def _call_params(self, **kwargs) -> None:
        self.resource_url = self._format_url_and_remove_params(kwargs)
        self.headers = {
            "User-Agent": USER_AGENT
        }
        self.params = kwargs
        self.params.update({
            'client_id': self.client.client_id,
            'app_version': self.client.app_version,
            'app_locale': self.client.app_locale
        })
        if self.client.authorization is not None:
            self.headers["Authorization"] = self.client.authorization

    def _load_href(self, url: str, param: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int]]:
        with requests.get(url, param, headers=self.headers, timeout=20) as req:
            if req.status_code not in [200, 201]:
                return {}
            req.raise_for_status()
            return req.json()

    def __call__(self, **kwargs) -> Optional[T]:
        self._call_params(**kwargs)
        data = self._load_href(self.resource_url, param=self.params)
        return _convert_dict(data, self.return_type)


@dataclass
class ListRequester(Requester, Generic[T]):
    """
    Class To Send Requests Which
    Returns List Of Return Type Data.
    """

    def __call__(self, **kwargs) -> List[T]:
        self._call_params(**kwargs)
        resources = []
        data = self._load_href(self.resource_url, param=self.params)
        for resource in data:
            resources.append(_convert_dict(resource, self.return_type))
        return resources


@dataclass
class CollectionRequester(Requester, Generic[T]):
    """
    Class To Send Requests Which
    Returns Collection Of Return Type Data.
    """

    def __call__(self, **kwargs):
        self._call_params(**kwargs)
        data = self._load_href(self.resource_url, self.params)
        par = {'client_id': self.client.client_id}
        while 'next_href' in data.keys() and data['next_href'] is not None and data['collection']:
            for result in data['collection']:
                yield _convert_dict(result, self.return_type)
            if 'next_href' in data.keys() and data['next_href'] is not None:
                data = self._load_href(data['next_href'], param=par)
