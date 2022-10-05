from enum import Enum

from .serializer import BaseSerializer
from ..message_types import MessageType


class EOASSPrePostSerializationProcessor:
    def pre_serialization(self, data: dict):
        if "Type" in data and isinstance(data["Type"], Enum):
            data["Type"] = data["Type"].value
        return data
    
    def post_deserialization(self, data: dict):
        if "Type" in data and isinstance(data["Type"], int):
            data["Type"] = MessageType(data["Type"])            
        return data
