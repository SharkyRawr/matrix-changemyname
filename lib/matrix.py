import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import requests

PUT_ROOM_STATE_API = r'/_matrix/client/r0/rooms/{roomid}/state/m.room.member/{userid}'
GET_PRESENCE_STATUS_API = r'/_matrix/client/r0/presence/{userid}/status'
GET_JOINED_ROOMS_API = r'/_matrix/client/r0/joined_rooms'
GET_ROOM_NAME_API = r'/_matrix/client/r0/rooms/{roomid}/state/m.room.name/'
GET_ROOM_MEMBERS_API = r'/_matrix/client/r0/rooms/{roomid}/members'
POST_MEDIA_UPLOAD_API = r'/_matrix/media/r0/upload'


class MatrixRoom(object):
    matrix = None

    def __init__(self, room_id: str, name: str = None) -> None:
        self.room_id = room_id
        self.name = name

    def __str__(self) -> str:
        if self.name:
            return self.name
        return self.room_id

    def has_name(self) -> bool:
        return self.name != None

    def set_name(self, name: str) -> None:
        self.name = name


class MatrixAPI(object):
    def __init__(self,  access_token: str = None,
                 homeserver: str = "https://matrix-client.matrix.org",
                 user_id: str = None,
                 ):
        self.access_token = access_token
        self.homeserver = homeserver
        self.user_id = user_id

    def set_token(self, access_token: str) -> None:
        self.access_token = access_token

    def do(self, method: str, url: str, json: dict = None, headers: Dict[str, str] = None, **kwargs):
        hdr = {
            'Authorization': r'Bearer {}'.format(self.access_token)
        }
        if headers is not None:
            hdr.update(headers)

        _rm = getattr(requests, method)
        r = _rm(urljoin(self.homeserver, url),
                json=json, headers=hdr, **kwargs)
        return r

    def save(self, statefile='settings.json') -> None:
        with open(statefile, 'w') as f:
            json.dump(dict(
                access_token=self.access_token,
                homeserver=self.homeserver,
                user_id=self.user_id
            ), f)

    def load(self, statefile='settings.json') -> bool:
        try:
            with open(statefile) as f:
                data: dict = json.load(f)
                for k in set(['access_token', 'homeserver', 'user_id']):
                    if k in data:
                        setattr(self, k, data[k])
            return True

        except FileNotFoundError:
            return False
        except Exception as ex:
            raise

    def get_presence(self, userid: str = None) -> Any:
        uid = userid or self.user_id

        r = self.do('get', GET_PRESENCE_STATUS_API.format(userid=uid))
        r.raise_for_status()
        return r.json()

    def update_roomstate(self, displayname: str = None, avatarmxc: str = None):
        args = {}
        if displayname:
            args['displayname'] = displayname
        if avatarmxc:
            args['avatar_url'] = avatarmxc

        if not displayname and not avatarmxc:
            raise AssertionError("What exactly are you trying to do?")

    def get_rooms(self) -> List[str]:
        r = self.do('get', GET_JOINED_ROOMS_API)
        r.raise_for_status()
        return r.json()['joined_rooms']

    def get_room_name(self, room: Union[MatrixRoom, str]) -> Optional[str]:
        r = self.do('get', GET_ROOM_NAME_API.format(
            roomid=room.room_id if type(room) is MatrixRoom else room))

        r.raise_for_status()

        data: dict = r.json()
        return data.get('name', None)

    def get_room_members(self, room: Union[MatrixRoom, str], exclude_myself: bool = False) -> List[str]:
        r = self.do('get', GET_ROOM_MEMBERS_API.format(
            roomid=room.room_id if type(room) is MatrixRoom else room))
        r.raise_for_status()

        data: dict = r.json()
        chunks: list = data['chunk']

        memberlist = []
        for chunk in chunks:
            if exclude_myself and chunk['sender'] == self.user_id:
                continue
            memberlist.append(chunk['content']['displayname'])

        return memberlist

    def upload_media(self, filename: str, content_type: str = None) -> str:
        from mimetypes import guess_type
        guessed_type, _ = guess_type(filename)
        ct = content_type or str(guessed_type)
        with open(filename, 'rb') as f:
            r = self.do('post', POST_MEDIA_UPLOAD_API, headers=dict(
                content_type=ct), params=dict(filename=filename), data=f)
        r.raise_for_status()
        return r.json()['content_uri']
