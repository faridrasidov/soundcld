"""
Request Handler Of SoundCld
"""
import string
import urllib.parse
from dataclasses import dataclass
from typing import Optional, Dict, Generic, TypeVar, get_origin, Union, List

import requests
from dacite import MissingValueError

from soundcld.resource.like import PlaylistLike, TrackLike
from soundcld.resource.playlist_album import AlbumPlaylist, BasicAlbumPlaylist
from soundcld.resource.stream_repost import (
    PlaylistStreamItem,
    PlaylistStreamRepostItem,
    TrackStreamItem,
    TrackStreamRepostItem)
from soundcld.resource.track import Track, BasicTrack
from soundcld.resource.user import User, BasicUser

T = TypeVar('T')


def _convert_dict(data, return_type: T):
    union = get_origin(return_type) is Union
    data_type = ''
    union_types = {
        'user': [User, BasicUser],
        'track': [Track, BasicTrack, TrackStreamItem],
        'playlist': [AlbumPlaylist, BasicAlbumPlaylist, PlaylistStreamItem],
        'like': [TrackLike, PlaylistLike],
        'playlist-repost': [PlaylistStreamRepostItem],
        'track-repost': [TrackStreamRepostItem]
    }
    if union:
        if 'kind' in data.keys():
            data_type = data['kind']
        if 'type' in data.keys():
            data_type = data['type']
        if data_type in union_types:
            for t in union_types[data_type]:
                try:
                    return t.from_dict(data)
                except MissingValueError:
                    pass
    else:
        return return_type.from_dict(data)
    raise ValueError(f"Could not convert {data} to type {return_type}")


@dataclass
class GetReq(Generic[T]):
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
        self.params = kwargs
        self.params.update({
            'client_id': self.client.data['client_id'],
            'app_version': self.client.data['app_version'],
            'app_locale': 'en'
        })

    def _load_href(self, url: str, param: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int]]:
        params = urllib.parse.urlencode(param, quote_via=urllib.parse.quote)
        with requests.get(url=url, params=params, timeout=20,
                          cookies=self.client.cookies,
                          headers=self.client.headers) as req:
            if req.status_code not in [200, 201]:
                print(f'Something Went Wrong. Error {req.status_code}')
                return {}
            req.raise_for_status()
            return req.json()

    def __call__(self, **kwargs) -> Optional[T]:
        self._call_params(**kwargs)
        data = self._load_href(self.resource_url, param=self.params)
        return _convert_dict(data, self.return_type)


@dataclass
class ListGetReq(GetReq, Generic[T]):
    """
    Class To Send Requests Which
    Returns List Of Return Type Data.
    """

    def __call__(self, **kwargs) -> List[T]:
        self._call_params(**kwargs)
        resources = []
        data = self._load_href(self.resource_url, param=self.params)
        if 'collection' not in data:
            for resource in data:
                resources.append(_convert_dict(resource, self.return_type))
        else:
            for ids in data['collection']:
                resources.append(ids)
        return resources


@dataclass
class CollectionGetReq(GetReq, Generic[T]):
    """
    Class To Send Requests Which
    Returns Collection Of Return Type Data.
    """

    def __call__(self, **kwargs):
        self._call_params(**kwargs)
        data = self._load_href(self.resource_url, self.params)
        while 'collection' in data.keys() and data['collection']:
            for result in data['collection']:
                yield _convert_dict(result, self.return_type)
            if 'next_href' in data.keys() and data['next_href'] is not None:
                data = self._load_href(data['next_href'], param=self.params)
            else:
                break
