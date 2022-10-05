from ctypes import Union
from threading import Lock
from types import FunctionType
from typing import BinaryIO
import uuid

from .protocol import BaseProtocol


class ConnectionSession:
    def __init__(self,
                 protocol: BaseProtocol,
                 connection_stream: BinaryIO = None,
                 write_func: FunctionType = None):
        self._protocol = protocol
        self._connection_stream = connection_stream
        self._write_func = write_func
        self._connection_lock = Lock()
        self._token = str(uuid.uuid4())

    @property
    def token(self):
        return self._token

    def send_data(self, data: dict):
        self._connection_lock.acquire()
        
        encoded_data = self._protocol.encode_message(data)        
        if self._connection_stream:
            self._connection_stream.write(encoded_data)
        elif self._write_func:
            self._write_func(encoded_data)
            
        self._connection_lock.release()
        
    def __str__(self) -> str:
        return str(self._token)
