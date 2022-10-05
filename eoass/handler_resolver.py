from typing import List
from eoass.message_types import MessageType
from .base_message_handler import BaseMessageHandler


class MessageHandlerResolver:
    def __init__(self):
        self._resolvers: List[BaseMessageHandler] = []

    def __getitem__(self, request_type: MessageType) -> List[BaseMessageHandler]:
        resolvers = []
        for resolver in self._resolvers:
            if resolver.message_type == request_type:
                resolvers.append(resolver)
        return resolvers

    def add_handler(self, handler: BaseMessageHandler):
        self._resolvers.append(handler)

    def remove_handler(self, handler: BaseMessageHandler):
        self._resolver.remove(handler)
