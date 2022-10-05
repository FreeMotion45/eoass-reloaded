from eoass.message_types import MessageType
from ....base_message_handler import BaseMessageHandler
from ..room import Room
from ..room_manager import RoomManager
from ....connection_session import ConnectionSession


class JoinRoomHandler(BaseMessageHandler):
    def __init__(self, room_manager):
        super(JoinRoomHandler, self).__init__(MessageType.JoinRoom)
        self._room_manager: RoomManager = room_manager

    def handle_message(self, request: dict, user_session: ConnectionSession):
        room_name_to_join: str = request["room_name"]
        room_to_join: Room = self._room_manager.find_room_with_name(room_name_to_join)
        if room_to_join is not None:
            if room_to_join.password is not None:
                if 'password' not in request:
                    print(f'@{user_session.token} didn\'t provide any password to join room {room_name_to_join}')
                    return
                if request['password'] != room_to_join.password:
                    print(f'@{user_session.token} password for room {room_name_to_join} is incorrect.')
                    return
            room_to_join.add_user(user_session)
            print(f'Successfully joined user @{user_session.token} to room {room_name_to_join}')
        else:
            print(f'Tried to join user @{user_session.token} to room {room_name_to_join} but it doesnt exist.')
