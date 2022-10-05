import socket
import time

from eoass.protocol import SimpleProtocol
from eoass.message_types import MessageType
from eoass.serialization.serializer import JsonSerializer


class Client:
    def __init__(self, ip, host):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((ip, host))
        self.protocol = SimpleProtocol(JsonSerializer())

    def send_join_room(self, room_name: str):
        msg = {
            "Type": MessageType.JoinRoom.value,
            "room_name": room_name,
        }

        self._client.send(self._input(msg))

    def send_join_room_pass(self, room_name: str, passw):
        msg = {
            "Type": MessageType.JoinRoom.value,
            "room_name": room_name,
            'password': passw,
        }

        self._client.send(self._input(msg))

    def create_room(self, room_name: str):
        msg = {
            "Type": MessageType.CreateRoom.value,
            "room_name": room_name,
        }

        self._client.send(self._input(msg))

    def create_room_pass(self, room_name: str, password):
        msg = {
            "Type": MessageType.CreateRoom.value,
            "room_name": room_name,
            'password': password,
        }

        self._client.send(self._input(msg))


    def leave_room(self):
        msg = {
            "Type": MessageType.LeaveRoom.value,
        }

        self._client.send(self._input(msg))

    def remove_room(self):
        msg = {
            "Type": MessageType.RemoveRoom.value,
        }

        self._client.send(self._input(msg))

    def _input(self, msg):
        return self.protocol.encode_message(msg)


client = Client("127.0.0.1", 45000)
client2 = Client("127.0.0.1", 45000)
client.create_room_pass("bluuu", '123123')
time.sleep(0.2)
client2.send_join_room('bluuu')
time.sleep(0.2)
client.leave_room()
time.sleep(0.2)
print("sent values")
