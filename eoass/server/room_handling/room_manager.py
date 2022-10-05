from typing import List

from ..room_handling.room import Room
from ...connection_session import ConnectionSession


class RoomManager:
    def __init__(self):
        self._rooms: List[Room] = []
        
    @property
    def rooms(self):
        return self._rooms.copy()

    def new_room(self, room: Room):
        if self.find_room_with_name(room.name) is None:
            self._rooms.append(room)
        else:
            raise NameError(f'Room with name: {room.name} already exists!')

    def remove_room_by_name(self, room_name: str):
        room_to_remove = self.find_room_with_name(room_name)
        if room_to_remove is not None:
            self._rooms.remove(room_to_remove)

    def find_room_with_name(self, name: str):
        for room in self._rooms:
            if room.name == name:
                return room
        return None

    def find_room_containing_user(self, user_session: ConnectionSession):
        for room in self._rooms:
            if room.contains_user(user_session):
                return room
        return None
