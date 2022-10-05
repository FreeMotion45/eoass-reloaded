from queue import Queue
import socket
from threading import Thread
from typing import AnyStr, List, Mapping
from eoass.client.handlers.music_player import MusicPlayer

from eoass.message_types import MessageType


from .handlers.music_data_handler import MusicDataHandler
from ..connection_session import ConnectionSession
from ..base_message_handler import BaseMessageHandler
from ..serialization.eoass_pre_post_serialization_processor import EOASSPrePostSerializationProcessor
from ..protocol import BaseProtocol


class EOASSClient:
    def __init__(self, host: AnyStr, protocol: BaseProtocol, player: MusicPlayer, port: int = 45000) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._proto = protocol
        self._host = host
        self._port = port
        self._music_data_handler = MusicDataHandler(player)
        self._receiver_thread = None
        self._sync_messages = Queue()
            
    def start(self):
        self._sock.connect((self._host, self._port))
        self._receiver_thread = Thread(target=self._receive_loop)
        self._receiver_thread.daemon = True
        self._receiver_thread.start()
        
    def wait(self):
        self._receiver_thread.join()
        
    def send_command(self, command: dict, wait: bool = True) -> dict:
        """Sends the command and blocks until a response is received.

        Args:
            command (dict): The command to send.

        Returns:
            dict: The servers response to the command.
        """
        self._sock.send(self._proto.encode_message(command))
        
        if wait:
            return self._sync_messages.get()
            
    def _receive_loop(self):
        server_session = ConnectionSession(self._proto, write_func=self._sock.send)
        
        while True:
            data = self._proto.read_next_message_from_func(self._sock.recv)
            
            if data["Type"] == MessageType.MusicData:
                self._music_data_handler.handle_message(data, server_session)
            else:
                self._sync_messages.put(data)
