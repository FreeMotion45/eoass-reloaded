import socketserver
from threading import Thread

from ..handler_resolver import MessageHandlerResolver
from .lobby_connection_handler import LobbyConnectionHandler
from ..protocol import BaseProtocol


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class LobbyServer:
    def __init__(self, ip: str, port: int,
                 command_resolver: MessageHandlerResolver = None,
                 protocol: BaseProtocol = None):
        self._server = ThreadedServer((ip, port), LobbyConnectionHandler)
        self._server.handler_resolver = command_resolver
        self._server.protocol = protocol

        self._server_thread = Thread(target=self._server.serve_forever)

    def start_async(self) -> None:
        self._server_thread.start()

    def close(self) -> None:
        self._server.shutdown()
        self._server_thread.join()
