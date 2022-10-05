from enum import Enum
import json
from abc import ABC, abstractmethod


class BaseSerializer(ABC):
    @abstractmethod
    def serialize(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, raw_data: bytes):
        raise NotImplementedError


class JsonSerializer(BaseSerializer):
    def serialize(self, data: dict):
        data_as_json = json.dumps(data)
        encoded_data = data_as_json.encode('utf-8')
        return encoded_data

    def deserialize(self, raw_data: bytes):
        decoded_raw_data = raw_data.decode('utf-8')
        return json.loads(decoded_raw_data)
