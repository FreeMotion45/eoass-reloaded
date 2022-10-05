from abc import ABC, abstractmethod

from .connection_session import ConnectionSession


class BaseMessageHandler(ABC):
    def __init__(self, message_type) -> None:
        super().__init__()
        self._message_type = message_type
    
    @abstractmethod
    def handle_message(self, message: dict, connection_session: ConnectionSession):
        ...
        
    @property
    def message_type(self):
        return self._message_type
