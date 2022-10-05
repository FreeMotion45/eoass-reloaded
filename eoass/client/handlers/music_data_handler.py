import base64
from queue import Queue
import pyaudio

from .music_player import MusicPlayer
from ...message_types import MessageType
from ...connection_session import ConnectionSession
from ...base_message_handler import BaseMessageHandler


_PLAY_TIME_BEFORE_REQUESTING_NEXT_CHUNK = 5


class MusicDataHandler(BaseMessageHandler):
    def __init__(self, player: MusicPlayer) -> None:
        super().__init__(MessageType.MusicData)
        self._player = player
    
    def handle_message(self, message: dict, user_session: ConnectionSession):
        self._player.receive_music_chunk(message, user_session)
        