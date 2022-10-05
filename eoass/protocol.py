import struct
from types import SimpleNamespace

from .serialization.eoass_pre_post_serialization_processor import EOASSPrePostSerializationProcessor

from .serialization.serializer import BaseSerializer

LENGTH_HEADER_SIZE = 4


class BaseProtocol:
    def __init__(self, serializer: BaseSerializer, pre_post_processor: EOASSPrePostSerializationProcessor):
        self._serializer = serializer
        self._pre_post_processor = pre_post_processor

    def encode_message(self, data: dict) -> bytes:
        raise NotImplementedError

    def read_next_message(self, stream) -> bytes:
        raise NotImplementedError
    
    def read_next_message_from_func(self, func) -> bytes:
        obj = SimpleNamespace(read=func)
        return self.read_next_message(obj)


class SimpleProtocol(BaseProtocol):
    def __init__(self, serializer: BaseSerializer, pre_post_processor: EOASSPrePostSerializationProcessor):
        # TODO: pre_post_processor should be taken care of in the base class.
        super().__init__(serializer, pre_post_processor)

    def encode_message(self, data: dict) -> bytes:
        post_processed = self._pre_post_processor.pre_serialization(data)
        
        encoded_data = self._serializer.serialize(data)
        data_length = len(encoded_data)        
        return struct.pack('<I', data_length) + encoded_data

    def read_next_message(self, stream) -> bytes:
        encoded_length = stream.read(LENGTH_HEADER_SIZE)
        if len(encoded_length) == 0:
            return None
        
        data_length = struct.unpack('<I', encoded_length)[0]
        remaining_data = data_length
        raw_data = b""
        while remaining_data > 0:
            raw_data += stream.read(remaining_data)
            remaining_data = data_length - len(raw_data)
        
        deserialized = self._serializer.deserialize(raw_data)
        post_deserialized = self._pre_post_processor.post_deserialization(deserialized)
        
        return post_deserialized
