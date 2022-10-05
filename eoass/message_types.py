from enum import Enum


class MessageType(Enum):
    JoinRoom = 1
    LeaveRoom = 2
    CreateRoom = 3
    RemoveRoom = 4
    MusicData = 5
    Welcome = 6
    MusicStreamContinue = 7
    ChangeMusicFile = 8

