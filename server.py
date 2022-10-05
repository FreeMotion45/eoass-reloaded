from pathlib import Path
import time
from threading import Event


from eoass.handler_resolver import MessageHandlerResolver
from eoass.serialization.eoass_pre_post_serialization_processor import EOASSPrePostSerializationProcessor
from eoass.server.lobby_server import LobbyServer
from eoass.protocol import SimpleProtocol
from eoass.server.room_handling.handlers.create_room_handler import CreateRoomHandler
from eoass.server.room_handling.handlers.join_room_handler import JoinRoomHandler
from eoass.server.room_handling.handlers.leave_room_handler import LeaveRoomHandler
from eoass.server.room_handling.handlers.music_stream_handling.music_storage import LocalFileSystemMusicStorage
from eoass.server.room_handling.handlers.music_stream_handling.music_stream_handlers import ChangeMusicHandler, MusicStreamContinueHandler
from eoass.server.room_handling.handlers.music_stream_handling.music_streamer_manager import MusicStreamerManager
from eoass.server.room_handling.handlers.remove_room_handler import RemoveRoomHandler
from eoass.server.room_handling.handlers.welcome_handler import WelcomeHandler
from eoass.server.room_handling.room import Room
from eoass.server.room_handling.room_manager import RoomManager
from eoass.serialization.serializer import JsonSerializer
from eoass.server.music_readers.wave_music_reader import WaveMusicReader


cmr = MessageHandlerResolver()


def add_room_handlers():
    room_manager = RoomManager()
    music_streamer_manager = MusicStreamerManager()
    music_storage = LocalFileSystemMusicStorage(Path(r"D:\Local\Programming\Python\EONSAS\music"))
    
    mr = WaveMusicReader(r"D:\Local\Programming\Python\EONSAS\music\Fitz and the Tantrums - A Place for Us [Official Audio].wav")
    music_room = Room("Music", None, mr)
    room_manager.new_room(music_room)
    
    cmr.add_handler(JoinRoomHandler(room_manager))
    cmr.add_handler(LeaveRoomHandler(room_manager))
    cmr.add_handler(CreateRoomHandler(room_manager))
    cmr.add_handler(RemoveRoomHandler(room_manager))
    cmr.add_handler(WelcomeHandler(room_manager, music_storage))
    cmr.add_handler(MusicStreamContinueHandler(music_streamer_manager))
    cmr.add_handler(ChangeMusicHandler(music_streamer_manager, music_storage))


add_room_handlers()


if __name__ == '__main__':
    server = LobbyServer("127.0.0.1", 45000, cmr, SimpleProtocol(JsonSerializer(), EOASSPrePostSerializationProcessor()))
    server.start_async()
    closed = Event()

    def close_server(signo, _frame):
        print('Closing all connections...')
        server.close()
        print('Server successfully shutdown.')
        closed.set()

    import signal
    signal.signal(signal.SIGINT, close_server)
    print('Server started!')
    while not closed.is_set():
        time.sleep(0.5)
    print('Bye! Have a great time!')
