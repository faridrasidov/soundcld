"""
SoundCld Is Soundcloud-v2 api handler
"""
from typing import List, Union

import soundcld.resource
from .api_handler import BaseSound


class SoundCloud(BaseSound):
    """
    The Main SoundCloud Class
    """

    def get_user(self, user_id: int):
        """
        Get User By User ID
        """
        link = f'/users/{user_id}'
        return self._get_user(link)

    def get_user_tracks(
            self,
            user_id: int,
            representation: str = '',
            limit: int = 20,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
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
        return self._get_tracks(link, **param)

    def get_user_top_tracks(self, user_id: int):
        """
        Get User's Top Tracks By User ID
        """
        link = f'/users/{user_id}/toptracks'
        return self._get_tracks(link)

    def get_user_albums(self, user_id: int):
        """
        Get User's Albums By User ID
        """
        link = f'/users/{user_id}/albums'
        return self._get_album_playlists(link)

    def get_user_playlists(self, user_id: int):
        """
        Get User's Playlists By User ID
        """
        link = f'/users/{user_id}/playlists_without_albums'
        return self._get_album_playlists(link)

    def get_user_likes(
            self,
            user_id: int,
            limit: int = 10,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get User's Likes By User ID
        """
        link = f'/users/{user_id}/likes'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_likes(link, **param)

    def get_user_streams(
            self,
            user_id: int,
            limit: int = 24
    ):
        """
        Get User's Streams/Reposts By User ID
        """
        link = f'/stream/users/{user_id}'
        param = {
            'offset': '',
            'limit': limit
        }
        return self._get_streams(link, **param)

    def get_user_reposts(
            self,
            user_id: int,
            limit: int = 24
    ):
        """
        Get User's Reposts By User ID
        """
        link = f'/stream/users/{user_id}/reposts'
        param = {
            'offset': '',
            'limit': limit
        }
        return self._get_reposts(link, **param)

    def get_user_comments(
            self,
            user_id: int,
            limit: int = 20,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get User's Comments By User ID
        """
        link = f'/users/{user_id}/comments'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_comments(link, **param)

    def get_related_artists(
            self,
            user_id: int,
            creators_only: bool = False,
            page_size: int = 12,
            limit: int = 12,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
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
        return self._get_users(link, **param)

    def get_user_followers(
            self,
            user_id: int,
            limit: int = 10,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get User's Follower Users By User ID
        """
        link = f'/users/{user_id}/followers'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_users(link, **param)

    def get_user_followings(self, user_id: int):
        """
        Get User's Following Users By User ID
        """
        link = f'/users/{user_id}/followings'
        return self._get_users(link)

    def get_user_followings_not_followed_by_user(
            self,
            user_id: int,
            target_id: int,
            limit: int = 3,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get User's Following Users,
        Which Not Followed By Target User
        """
        link = f'/users/{user_id}/followings/not_followed_by/{target_id}'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_users(link, **param)

    def get_user_followers_followed_by_user(
            self,
            user_id: int,
            target_id: int,
            limit: int = 10,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get User's Follower Users,
        Which Followed By Target User
        """
        link = f'/users/{user_id}/followers/followed_by/{target_id}'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_users(link, **param)

    def get_track(self, track_id: int):
        """
        Get Track By Track ID
        """
        link = f'/tracks/{track_id}'
        return self._get_track(link)

    def get_tracks(self, track_ids: List[int]):
        """
        Get Multiple Tracks By Track IDs
        """
        link = '/tracks'
        param = {
            'ids': ','.join([str(its) for its in track_ids]),
            '%5Bobject%20Object%5D': ''
        }
        return self._get_track_list(link, **param)

    def get_track_liker(self, track_id: int):
        """
        Get Track's Liker Users By Track ID
        """
        link = f'/tracks/{track_id}/likers'
        return self._get_users(link)

    def get_track_reposter(self, track_id: int):
        """
        Get Track's Reposter Users By Track ID
        """
        link = f'/tracks/{track_id}/reposters'
        return self._get_users(link)

    def get_track_comments(
            self,
            track_id: int,
            threaded: int = 1,
            limit: int = 200,
            offset: int = 0,
            linked_partitioning: int = 1,
            sort: str = 'newest'
    ):
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
        return self._get_basic_comments(link, **param)

    def get_related_tracks(self, track_id: int):
        """
        Get Related Tracks By Track ID
        """
        link = f'/tracks/{track_id}/related'
        return self._get_tracks(link)

    def get_track_by_tag(self, tag: str):
        """
        Get Recent Tracks With Tag Word
        """
        link = f'/recent-tracks/{tag}'
        return self._get_tracks(link)

    def get_playlist(self, playlist_id: int):
        """
        Get Playlist By Playlist ID
        """
        link = f'/playlists/{playlist_id}'
        return self._get_album_playlist(link)

    def get_playlist_liker(self, playlist_id: int):
        """
        Get Playlist's Liker Users By Playlist ID
        """
        link = f'/playlists/{playlist_id}/likers'
        return self._get_users(link)

    def get_playlist_reposter(self, playlist_id: int):
        """
        Get Playlist's Reposter Users By Playlist ID
        """
        link = f'/playlists/{playlist_id}/reposters'
        return self._get_users(link)

    def get_albums_with_track(self, track_id: int):
        """
        Get Albums Where Track ID Have Been Added
        """
        link = f'/tracks/{track_id}/albums'
        return self._get_album_playlists(link)

    def get_playlists_with_track(self, track_id: int):
        """
        Get Playlists Where Track ID Have Been Added
        """
        link = f'/tracks/{track_id}/playlists_without_albums'
        return self._get_album_playlists(link)

    def get_search_all(
            self,
            text: str,
            facet: str = 'model',
            variant_ids: str = '',
            limit: int = 20,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get All Search Result {User, Track,
        Playlist, Album} By Text To Search
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
        return self._get_searches(link, **param)

    def get_search_tracks(
            self,
            text: str,
            facet: str = 'genre',
            variant_ids: str = '',
            limit: int = 20,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
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
        return self._get_searches(link, **param)

    def get_search_users(
            self,
            text: str,
            facet: str = 'place',
            variant_ids: str = '',
            limit: int = 20,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
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
        return self._get_searches(link, **param)

    def get_search_albums(
            self,
            text: str,
            facet: str = 'genre',
            variant_ids: str = '',
            limit: int = 20,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
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
        return self._get_searches(link, **param)

    def get_search_playlists(
            self,
            text: str,
            facet: str = 'genre',
            variant_ids: str = '',
            limit: int = 20,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
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
        return self._get_searches(link, **param)

    def get_web_profiles(self, user_id: int):
        """
        Get User's WebProfiles Users By User ID
        """
        if not user_id and self.is_logged_in():
            user_id = self.my_account_id
        link = f'/users/soundcloud:users:{user_id}/web-profiles'
        return self._get_web_profile_list(link)

    def get_my_tracks(self):
        """
        Get My {Logged-In User} Tracks
        """
        return self.get_user_tracks(self.my_account_id, representation='owner')

    def get_user_followings_not_followed_by_me(
            self,
            user_id: int,
            limit: int = 3,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get User's Following Users,
        Which Not Followed By Me {Logged-In User}
        """
        link = f'/users/{user_id}/followings/not_followed_by/{self.my_account_id}'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_users(link, **param)

    def get_user_followers_followed_by_me(
            self,
            user_id: int,
            limit: int = 10,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get User's Follower Users,
        Which Followed By Me {Logged-In User}
        """
        link = f'/users/{user_id}/followers/followed_by/{self.my_account_id}'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_users(link, **param)

    def get_my_user_conversation(
            self,
            user_id: int,
            limit: int = 10,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get My {Logged-In User} Conversation Messages By User ID
        """
        link = f'/users/{self.my_account_id}/conversations/{user_id}/messages'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_conversation_messages(link, **param)

    def get_my_conversations_thumb(
            self,
            limit: int = 10,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get My {Logged-In User} Conversations Thumb {Last Message}
        """
        link = f'/users/{self.my_account_id}/conversations'
        param = {
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_conversations(link, **param)

    def get_my_unread_conversations(
            self,
            force: int = 1,
            limit: int = 20,
            offset: int = 0,
            linked_partitioning: int = 1
    ):
        """
        Get My {Logged-In User} Unread Conversations
        """
        link = f'/users/{self.my_account_id}/conversations/unread'
        param = {
            'force': force,
            'limit': limit,
            'offset': offset,
            'linked_partitioning': linked_partitioning
        }
        return self._get_conversations(link, **param)

    def get_my_streams(self, limit: int = 24):
        """
        Get My {Logged-In User} Streams/Reposts By User ID
        """
        link = f'/stream/users/{self.my_account_id}'
        param = {
            'offset': '',
            'limit': limit
        }
        return self._get_streams(link, **param)

    def get_my_reposts(self, limit: int = 24):
        """
        Get My {Logged-In User} Reposts
        """
        link = f'/stream/users/{self.my_account_id}/reposts'
        param = {
            'offset': '',
            'limit': limit
        }
        return self._get_reposts(link, **param)

    def get_my_liked_track_ids(self, limit: int = 200):
        """
        Get My {Logged-In User} Liked Tracks IDs
        """
        link = '/me/track_likes/ids'
        param = {
            'offset': '',
            'limit': limit
        }
        return self._get_id_list(link, **param)

    def get_my_track_reposts_ids(self, limit: int = 200):
        """
        Get My {Logged-In User} Track Reposts IDs
        """
        link = '/me/track_reposts/ids'
        param = {
            'limit': limit
        }
        return self._get_id_list(link, **param)

    def get_my_liked_playlist_ids(
            self,
            limit: int = 5000,
            linked_partitioning: int = 1
    ):
        """
        Get My {Logged-In User} Liked Playlist IDs
        """
        link = '/me/playlist_likes/ids'
        param = {
            'limit': limit,
            'linked_partitioning': linked_partitioning
        }
        return self._get_id_list(link, **param)

    def get_my_playlist_reposts_ids(self, limit: int = 200):
        """
        Get My {Logged-In User} Playlist Reposts IDs
        """
        link = '/me/playlist_reposts/ids'
        param = {
            'limit': limit
        }
        return self._get_id_list(link, **param)

    def get_my_followers_ids(
            self,
            limit: int = 5000,
            linked_partitioning: int = 1
    ):
        """
        Get My {Logged-In User} Followers IDs
        """
        link = '/me/followers/ids'
        param = {
            'limit': limit,
            'linked_partitioning': linked_partitioning
        }
        return self._get_id_list(link, **param)

    def get_my_following_ids(
            self,
            limit: int = 5000,
            linked_partitioning: int = 1
    ):
        """
        Get My {Logged-In User} Followings IDs.
        """
        link = f'/users/{self.my_account_id}/followings/ids'
        param = {
            'limit': limit,
            'linked_partitioning': linked_partitioning
        }
        return self._get_id_list(link, **param)

    def change_my_profile_info(
            self,
            permalink: str = None,
            username: str = None,
            city: str = None,
            country_code: str = None,
            description: str = None,
            first_name: str = None,
            last_name: str = None
    ):
        """
        Changes My {Logged-In User} Information.
        """
        link = '/me'
        last_info = self.get_user(self.my_account_id)
        payload = {
            'city': city,
            'country_code': country_code,
            'description': description,
            'first_name': first_name,
            'last_name': last_name,
            'permalink': permalink,
            'username': username
        }
        for item, value in payload.items():
            if not value:
                payload[item] = last_info[item]
        return self._put_payload(link, **payload)

    def like_track(self, track_id: int):
        """
        Likes The Track by Me {Logged-In User}.
        """
        link = f'/users/{self.my_account_id}/track_likes/{track_id}'
        return self._put_payload(link)

    def like_playlist(self, playlist_id: int):
        """
        Likes The Playlist or Album by Me {Logged-In User}.
        """
        link = f'/users/{self.my_account_id}/playlist_likes/{playlist_id}'
        return self._put_payload(link)

    def dislike_track(self, track_id: int):
        """
        Dislikes The Track by Me {Logged-In User}.
        """
        link = f'/users/{self.my_account_id}/track_likes/{track_id}'
        return self._delete_payload(link)

    def dislike_playlist(self, playlist_id: int):
        """
        Dislikes The Playlist or Album by Me {Logged-In User}.
        """
        link = f'/users/{self.my_account_id}/playlist_likes/{playlist_id}'
        return self._delete_payload(link)

    def create_playlist(
            self,
            playlist_name: str,
            trak_id: Union[int, List[int]],
            is_public: bool = True
    ):
        """
        Creates The Playlist by Me {Logged-In User}.
        """
        link = f'/playlists'
        payload = {
            'playlist': {
                'title': playlist_name,
                'tracks': [trak_id],
                '_resource_id': 'f-',
                '_resource_type': 'playlist'
            }
        }
        if is_public:
            payload['sharing'] = 'public'
        else:
            payload['sharing'] = 'private'
        return self._post_payload(link, **payload)

    def delete_playlist(self, playlist_id: int):
        """
        Removes The Playlist by Me {Logged-In User}.
        """
        link = f'/playlists/{playlist_id}'
        return self._delete_payload(link)
