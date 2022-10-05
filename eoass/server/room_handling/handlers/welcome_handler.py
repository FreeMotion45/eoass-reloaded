from .music_stream_handling.music_storage import LocalFileSystemMusicStorage
from ....connection_session import ConnectionSession
from ....message_types import MessageType
from ....base_message_handler import BaseMessageHandler
from ...room_handling.room import Room
from ...room_handling.room_manager import RoomManager
from ....connection_session import ConnectionSession


class WelcomeHandler(BaseMessageHandler):
    def __init__(self, room_manager, storage: LocalFileSystemMusicStorage):
        super(WelcomeHandler, self).__init__(MessageType.Welcome)
        self._room_manager: RoomManager = room_manager
        self._storage = storage

    def handle_message(self, request: dict, user_session: ConnectionSession):
        welcome_message = """Hello, and welcome to EOASS - Emanuels Online Audio Streaming Service.
Please enjoy your stay :).
        """
        
        # The welcome message also contains the available rooms.
        welcome_message = {
            "Type": MessageType.Welcome,
            "welcome_message": welcome_message,
            "rooms": [],
            "files": [],
        }
        for room in self._room_manager.rooms:
            welcome_message["rooms"].append({
                "name": room.name,
                "owner": room.owner,
                "requires_password": False if room.password is None else True,
            })
        for file in self._storage.get_all():
            welcome_message["files"].append(file)
        
        user_session.send_data(welcome_message)
