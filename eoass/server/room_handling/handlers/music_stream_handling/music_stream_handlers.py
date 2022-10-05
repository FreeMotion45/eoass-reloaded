from .....connection_session import ConnectionSession
from .....message_types import MessageType
from .....base_message_handler import BaseMessageHandler
from .music_streamer_manager import MusicStreamerManager
from .music_storage import LocalFileSystemMusicStorage


class MusicStreamContinueHandler(BaseMessageHandler):
    def __init__(self, music_streamer_manager: MusicStreamerManager):
        super(MusicStreamContinueHandler, self).__init__(MessageType.MusicStreamContinue)
        self._music_streamer_manager = music_streamer_manager

    def handle_message(self, request: dict, connection_session: ConnectionSession):
        self._music_streamer_manager[connection_session].stream_next_chunk()
        

class ChangeMusicHandler(BaseMessageHandler):
    def __init__(self, music_streamer_manager: MusicStreamerManager, storage: LocalFileSystemMusicStorage):
        super(ChangeMusicHandler, self).__init__(MessageType.ChangeMusicFile)
        self._music_streamer_manager = music_streamer_manager
        self._storage = storage

    def handle_message(self, request: dict, connection_session: ConnectionSession):
        file_name = request["file_name"]
        print(connection_session, 'requested to play:', file_name)
        
        music_reader = self._storage.get_music_reader(file_name)
        if music_reader is None:
            print(file_name, "doesnt exist in the music storage.")
            connection_session.send_data({
                "Type": MessageType.ChangeMusicFile,
                "success": False,
            })
            return
            
        print(connection_session, 'changed current track to:', file_name)
        self._music_streamer_manager[connection_session].replace_reader(music_reader)
        
        connection_session.send_data({
            "Type": MessageType.ChangeMusicFile,
            "success": True,
        })
