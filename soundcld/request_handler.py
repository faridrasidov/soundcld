"""
Request Handler Of SoundCld
"""
import json
import urllib.parse
from dataclasses import dataclass
from typing import Optional, Dict, Generic, TypeVar, get_origin, Union, List

import requests
from dacite import MissingValueError

from soundcld.resource import (
    PlaylistLike, TrackLike,
    AlbumPlaylist, BasicAlbumPlaylist,
    PlaylistStreamItem, PlaylistStreamRepostItem,
    TrackStreamItem, TrackStreamRepostItem,
    Track, BasicTrack,
    User, BasicUser
)

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
class BaseReq(Generic[T]):
    """
    Core Class To Send Request To Soundcloud
    """
    base = "https://api-v2.soundcloud.com"
    resource_url = params = headers = ''
    client: T
    format_url: str

    def _call_params(self, **kwargs) -> None:
        self.resource_url = self.base + self.format_url
        self.params = kwargs
        self.params.update({
            'client_id': self.client.data['client_id'],
            'app_version': self.client.data['app_version'],
            'app_locale': 'en'
        })


@dataclass
class GetReq(BaseReq, Generic[T]):
    """
    Core Class To Send GET Request
    To Soundcloud
    """
    return_type: T

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
    Class To Send GET Requests Which
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
    Class To Send GET Requests Which
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


@dataclass
class ComplexReq:
    """
    Core Class To Handle Complex
    Requests Common Functionality.
    """

    def _load_option(self, client, url, payload):
        self.complex_cookies = client.cookies
        self.complex_headers = client.headers
        self.complex_headers['Content-Length'] = '0'
        self.complex_headers['x-datadome-clientid'] = client.cookies['datadome']
        if payload:
            my_payload = json.dumps(payload)
            my_payload = my_payload.replace(': "', ':"')
            my_payload = my_payload.replace(', ', ',')
            self.complex_headers['Content-Length'] = f'{len(my_payload)}'
        with requests.options(
                url=url,
                timeout=20,
                cookies=self.complex_cookies,
                headers=self.complex_headers
        ) as req:
            if not f'{req.status_code}'.startswith('2'):
                print(f'Something Went Wrong. Can\'t Get Options.'
                      f'Error {req.status_code}')
                return {'status': 'err'}
            else:
                print(f'option : {req.status_code} : {req.text}')
            req.raise_for_status()

    @staticmethod
    def _update_datadome(req: requests.Response, client):
        if 'x-set-cookie' in req.headers.keys():
            x_set_cookie = req.headers['x-set-cookie']
            x_set_cookie = x_set_cookie.split(';')
            for item in x_set_cookie:
                if 'datadome' in item:
                    x_set_datadome_cookie = item.split('=')[1]
                    client.cookies['datadome'] = x_set_datadome_cookie
                    break


@dataclass
class PutReq(BaseReq, ComplexReq):
    """
    Core Class To Send PUT Request
    To Soundcloud
    """

    def _load_href(
            self,
            url: str,
            param: dict,
            payload: dict
    ) -> Dict:
        params = urllib.parse.urlencode(
            param,
            quote_via=urllib.parse.quote
        )
        self._load_option(client=self.client, url=url, payload=payload)
        req = requests.put(
            url=url,
            params=params,
            json=payload,
            timeout=20,
            cookies=self.complex_cookies,
            headers=self.complex_headers
        )
        self._update_datadome(req=req, client=self.client)
        if not f'{req.status_code}'.startswith('2'):
            print(f'Something Went Wrong. Error {req.status_code}')
            return {'status': 'err'}
        print(f'putting : {req.status_code} : {req.text}')
        req.raise_for_status()
        return {'status': 'ok'}

    def __call__(self, **kwargs):
        self._call_params(**kwargs)
        data = self._load_href(self.resource_url, self.params, kwargs)
        if data['status'] == 'ok':
            print('User Information Updated.')
        else:
            print('User Information Not Updated.')


@dataclass
class DeleteReq(BaseReq, ComplexReq):
    """
    Core Class To Send Delete Request
    To Soundcloud
    """

    def _load_href(
            self,
            url: str,
            param: dict,
            payload: dict
    ) -> Dict:
        params = urllib.parse.urlencode(
            param,
            quote_via=urllib.parse.quote
        )
        self._load_option(client=self.client, url=url, payload=payload)
        req = requests.delete(
            url=url,
            params=params,
            json=payload,
            timeout=20,
            cookies=self.complex_cookies,
            headers=self.complex_headers
        )
        self._update_datadome(req=req, client=self.client)
        if not f'{req.status_code}'.startswith('2'):
            print(f'Something Went Wrong. Error {req.status_code}')
            return {'status': 'err'}
        print(f'deleting : {req.status_code} : {req.text}')
        req.raise_for_status()
        return {'status': 'ok'}

    def __call__(self, **kwargs):
        self._call_params(**kwargs)
        data = self._load_href(self.resource_url, self.params, kwargs)
        if data['status'] == 'ok':
            print('User Information Updated.')
        else:
            print('User Information Not Updated.')


@dataclass
class PostReq(BaseReq, ComplexReq):
    """
    Core Class To Send Post Request
    To Soundcloud
    """

    def _load_href(
            self,
            url: str,
            param: dict,
            payload: dict
    ) -> Dict:
        params = urllib.parse.urlencode(
            param,
            quote_via=urllib.parse.quote
        )
        self._load_option(client=self.client, url=url, payload=payload)
        req = requests.post(
            url=url,
            params=params,
            json=payload,
            timeout=20,
            cookies=self.complex_cookies,
            headers=self.complex_headers
        )
        self._update_datadome(req=req, client=self.client)
        if not f'{req.status_code}'.startswith('2'):
            print(f'Something Went Wrong. Error {req.status_code}')
            return {'status': 'err'}
        print(f'posting : {req.status_code} : {req.text}')
        req.raise_for_status()
        return {'status': 'ok'}

    def __call__(self, **kwargs):
        self._call_params(**kwargs)
        data = self._load_href(self.resource_url, self.params, kwargs)

        if data['status'] == 'ok':
            print('User Information Updated.')
        else:
            print('User Information Not Updated.')
