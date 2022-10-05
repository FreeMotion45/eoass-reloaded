from typing import Mapping

from .music_session_streamer import MusicSessionStreamer
from .....connection_session import ConnectionSession


class MusicStreamerManager:
    def __init__(self) -> None:
        self._music_streamers: Mapping[ConnectionSession, MusicSessionStreamer] = dict()
        
    def __getitem__(self, user: ConnectionSession) -> MusicSessionStreamer:
        if user not in self._music_streamers:
            self._music_streamers[user] = MusicSessionStreamer(user)
        return self._music_streamers[user]