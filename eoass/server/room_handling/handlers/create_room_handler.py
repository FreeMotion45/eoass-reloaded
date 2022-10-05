from ....message_types import MessageType
from ....base_message_handler import BaseMessageHandler
from ..room import Room
from ..room_manager import RoomManager
from ....connection_session import ConnectionSession


class CreateRoomHandler(BaseMessageHandler):
    def __init__(self, room_manager):
        super(CreateRoomHandler, self).__init__(MessageType.CreateRoom)
        self._room_manager: RoomManager = room_manager

    def handle_message(self, request: dict, user_session: ConnectionSession):
        present_room = self._room_manager.find_room_containing_user(user_session)
        is_present_in_other_room = present_room is not None
        if is_present_in_other_room:
            print(f'User @{user_session.token} can not create room before leaving room {present_room.name}')
            return

        room_name = request['room_name']
        room = Room(room_name, user_session)
        if 'password' in request:
            room.password = request['password']

        try:
            self._room_manager.new_room(room)
            print(f'User @{user_session.token} created a room {room_name}')
        except NameError as e:
            print(f'User @{user_session.token} tried to created a room with name {room_name} '
                  f'but a room with this name already exists!')
