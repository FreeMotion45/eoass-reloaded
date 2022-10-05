import base64
from queue import Queue
import pyaudio

from ...message_types import MessageType
from ...connection_session import ConnectionSession
from ...base_message_handler import BaseMessageHandler


_PLAY_TIME_BEFORE_REQUESTING_NEXT_CHUNK = 5


class MusicPlayer:
    def __init__(self) -> None:
        self._pyaudio = pyaudio.PyAudio()
        self._pyaudio_stream = None
        self._data_queue = Queue()
        self._metadata = dict()
        self._current_music_data = b""
        self._current_message = dict()
        self._pos_in_current = 0
        self._requested_next_chunk = False
        self._server: ConnectionSession = None
        
    def __del__(self):
        if self._pyaudio_stream is not None:
            if not self._pyaudio_stream.is_stopped():
                self._pyaudio_stream.stop_stream()
            self._pyaudio_stream.close()
        self._pyaudio.terminate()
        
    def resume(self):
        if self._pyaudio_stream and self._pyaudio_stream.is_stopped():
            self._pyaudio_stream.start_stream()
        
    def pause(self):
        if self._pyaudio_stream and not self._pyaudio_stream.is_stopped():
            self._pyaudio_stream.stop_stream()
            
    def clean(self):
        if self._pyaudio_stream is not None:
            if not self._pyaudio_stream.is_stopped():
                self._pyaudio_stream.stop_stream()
            self._pyaudio_stream.close()
            
            self._pyaudio_stream = None
            self._current_message = None
            self._current_music_data = b""
            self._pos_in_current = 0
                
    
    def receive_music_chunk(self, message: dict, user_session: ConnectionSession):
        if not self._server:
            self._server = user_session
            
        inserted_data = False
        
        if self._pyaudio_stream is None or self._metadata != message["Metadata"]:
            if self._pyaudio_stream is not None:
                self._pyaudio_stream.stop_stream()
                self._pyaudio_stream.close()
                
            self._clear_data_queue()
            inserted_data = True
            self._data_queue.put(message)
                
            self._metadata = message["Metadata"]
            self._pyaudio_stream = self._pyaudio.open(format=self._pyaudio.get_format_from_width(self._metadata["sample_width"]),
                                                      channels=self._metadata["channels"],
                                                      rate=self._metadata["framerate"],
                                                      output=True,
                                                      stream_callback=self._pyaudio_stream_callback)
            self._pyaudio_stream.start_stream()
            
        if not inserted_data:
            self._data_queue.put(message)
            
        # A chunk of data has arrived, therefore we are not already requesting more.
        self._requested_next_chunk = False
        
    def _clear_data_queue(self):
        while not self._data_queue.empty():
            self._data_queue.get()
            
    def _pyaudio_stream_callback(self, in_data, frame_count, time_info, status):
        if self._remaining_play_time < _PLAY_TIME_BEFORE_REQUESTING_NEXT_CHUNK:
            self._request_next_chunk()

        bytes_requested_count = self._metadata["sample_width"] * self._metadata["channels"] * frame_count
        bytes_to_return = b""
        
        while len(bytes_to_return) < bytes_requested_count:
            bytes_remaining_count = bytes_requested_count - len(bytes_to_return)
            
            upper_index = min(len(self._current_music_data), self._pos_in_current + bytes_remaining_count)
            bytes_to_return += self._current_music_data[self._pos_in_current:upper_index]
            self._pos_in_current = upper_index
            
            if self._pos_in_current == len(self._current_music_data):
                self._current_message = self._data_queue.get()
                self._current_music_data = base64.decodebytes(self._current_message["Data"].encode('utf-8'))
                self._pos_in_current = 0
            
            bytes_remaining_count = bytes_requested_count - len(bytes_to_return)
        
        return (bytes_to_return, pyaudio.paContinue)
    
    @property
    def _remaining_play_time(self):
        """Remains the remaining available audio time in the client buffer
        """        
        frames_left_in_current = (len(self._current_music_data) - self._pos_in_current) / (self._metadata["sample_width"] * self._metadata["channels"])
        time_left_in_current = frames_left_in_current / self._metadata["framerate"]
        
        # Each item in the data queue is an audio chunk whose size is 10 seconds.
        return time_left_in_current + self._data_queue.qsize() * 10
    
    def _request_next_chunk(self):
        # Only request the next chunk if we haven't done it before
        if not self._requested_next_chunk:
            self._requested_next_chunk = True            
            
            data = { "Type": MessageType.MusicStreamContinue }
            self._server.send_data(data)
        