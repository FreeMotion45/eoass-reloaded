import base64
from queue import Queue
from threading import Lock, Thread
from typing import Union

from ....music_readers.base_music_reader import BaseMusicReader
from .....connection_session import ConnectionSession
from .....message_types import MessageType

class MusicSessionStreamer:
    
    # There is no pause because pausing is a client side action.
    # To pause, basically means that the client won't send _CMD_CONTINUE.
    _CMD_CONTINUE = 1
    _CMD_REPLACE = 2
    _CMD_TERMINATE = 3
    
    def __init__(self, user_session: ConnectionSession) -> None:
        self._user = user_session
        self._music_reader: Union[None, BaseMusicReader] = None
        self._music_reader_lock = Lock()
        
        self._queue = Queue()
        
        self._stream_thread = Thread(target=self._stream_loop)
        self._stream_thread.daemon = True
        self._stream_thread.start()
    
    def replace_reader(self, music_reader: BaseMusicReader):
        self._music_reader_lock.acquire()
        self._music_reader = music_reader
        self._music_reader_lock.release()
        
    def stream_next_chunk(self):
        self._queue.put(MusicSessionStreamer._CMD_CONTINUE)
        
    def _stream_loop(self):
        while True:
            cmd = self._queue.get()
            if cmd == MusicSessionStreamer._CMD_TERMINATE:
                break
            
            if cmd == MusicSessionStreamer._CMD_CONTINUE:
                self._music_reader_lock.acquire()
                data = {
                    "Type": MessageType.MusicData,
                    "Data": base64.encodebytes(self._music_reader.read(10 * 1000)).decode('utf-8'),
                    "Metadata": self._music_reader.metadata
                }
                self._music_reader_lock.release()
                self._user.send_data(data)
                
    def __del__(self):
        self._queue.put(MusicSessionStreamer._CMD_TERMINATE)
        self._stream_thread.join()