import base64
from threading import Thread
import time
from typing import List

from ...message_types import MessageType
from ..music_readers.base_music_reader import BaseMusicReader
from ...connection_session import ConnectionSession


class Room:
    def __init__(self, 
                 name: str,
                 owner_user: ConnectionSession,
                 music_reader: BaseMusicReader,
                 password: str = None):
        self._users: List[ConnectionSession] = [owner_user]
        self._name = name
        self._owner = owner_user
        self._music_reader = music_reader
        self._password = password
        self._room_thread = Thread(target=self._room_thread_loop)
        self._room_thread.daemon = True
        self._room_thread.start()

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = new_password

    @property
    def owner(self) -> ConnectionSession:
        return self._owner

    @owner.setter
    def owner(self, new_owner: ConnectionSession):
        self._owner = new_owner

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, room_name):
        self._name = room_name

    def add_user(self, user: ConnectionSession):
        self._users.append(user)

    def remove_user(self, user: ConnectionSession):
        if user in self._users:
            self._users.remove(user)
            if user == self._owner and len(self._users) > 0:
                self._owner = self._users[0]
                print(f'The owner of room {self._name} has left. Automatically assigning @{self._owner.token} as the '
                      f'new owner.')
        else:
            raise Exception(f'ConnectionSession {user.token} can not be removed from the room {self._name} '
                            f'because it was not in the room.')

    def get_users(self) -> List[ConnectionSession]:
        return self._users.copy()

    def contains_user(self, user: ConnectionSession):
        return user in self._users
    
    def _room_thread_loop(self):
        while True:
            if len(self._users) == 0 or self._users == [None] * len(self._users):
                time.sleep(1)
                continue
            
            if not self._music_reader.finished:
                chunk = self._music_reader.read(2 * 1000)
                metadata = self._music_reader.metadata
                
                threads: List[Thread] = [self._send_chunk_async(user, chunk, metadata) for user in self._users if user is not None]
                for thread in threads:
                    thread.join()
            
                time.sleep(1)
            else:
                break
                
            
    def _send_data(self, user: ConnectionSession, data: dict):
        user.send_data(data)
        
    def _send_chunk(self, user: ConnectionSession, chunk: bytes, metadata: dict):
        data = dict()
        data['Type'] = MessageType.MusicData
        data['Metadata'] = metadata
        data['Data'] = base64.encodebytes(chunk).decode('utf-8')
        user.send_data(data)
        
    def _send_chunk_async(self, user: ConnectionSession, chunk: bytes, metadata: dict) -> Thread:
        thread = Thread(target=self._send_chunk, args=(user, chunk, metadata))
        thread.start()
        return thread
