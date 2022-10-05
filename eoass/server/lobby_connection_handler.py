import socketserver

from ..connection_session import ConnectionSession
from ..handler_resolver import MessageHandlerResolver
from ..message_types import MessageType
from ..protocol import BaseProtocol

LENGTH_HEADER_SIZE = 4


class LobbyConnectionHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        server = self.server
        self._protocol: BaseProtocol = server.protocol
        self._handler_resolver: MessageHandlerResolver = server.handler_resolver
        self._user_session: ConnectionSession = ConnectionSession(self._protocol, connection_stream=self.wfile)
        self._start_processing_requests()
        
    def _call_handlers(self, request_type: MessageType, request: dict):
        for resolver in self._handler_resolver[request_type]:
            resolver.handle_message(request, self._user_session)

    def _start_processing_requests(self):
        request: dict = self._protocol.read_next_message(self.rfile)
        while request is not None:
            self._process_request(request)
            request: dict = self._protocol.read_next_message(self.rfile)
            
        print("Connection closed....")
        self._call_handlers(MessageType.LeaveRoom, {})

    def _process_request(self, request: dict):
        request_type = request["Type"]
        self._call_handlers(request_type, request)
