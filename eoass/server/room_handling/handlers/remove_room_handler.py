from ....connection_session import ConnectionSession
from ....message_types import MessageType
from ....base_message_handler import BaseMessageHandler
from ..room_manager import RoomManager


class RemoveRoomHandler(BaseMessageHandler):
    def __init__(self, room_manager):
        super(RemoveRoomHandler, self).__init__(MessageType.RemoveRoom)
        self._room_manager: RoomManager = room_manager

    def handle_message(self, request: dict, user_session: ConnectionSession):
        room_to_remove = self._room_manager.find_room_containing_user(user_session)
        if room_to_remove.owner == user_session:
            self._room_manager.remove_room_by_name(room_to_remove.name)
            print(f'Room {room_to_remove.name} has been disbanded by @{user_session.token}')
