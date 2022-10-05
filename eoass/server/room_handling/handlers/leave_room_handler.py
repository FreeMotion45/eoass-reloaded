from eoass.message_types import MessageType
from ....base_message_handler import BaseMessageHandler
from ..room import Room
from ..room_manager import RoomManager
from ....connection_session import ConnectionSession


class LeaveRoomHandler(BaseMessageHandler):
    def __init__(self, room_manager):
        super(LeaveRoomHandler, self).__init__(MessageType.LeaveRoom)
        self._room_manager: RoomManager = room_manager

    def handle_message(self, request: dict, user_session: ConnectionSession):
        room_to_leave: Room = self._room_manager.find_room_containing_user(user_session)
        if room_to_leave is not None:
            if len(room_to_leave.get_users()) == 1:
                # This user is the last user to leave the room. Therefore we need to remove the room.
                self._room_manager.remove_room_by_name(room_to_leave.name)
                print(f'The last user of room {room_to_leave.name} has left the room. Removing the room...')
                return

            room_to_leave.remove_user(user_session)
            print(f'Successfully removed @{user_session.token} from room: {room_to_leave.name}')
        else:
            print(f'User @{user_session.token} is not in any room.')
