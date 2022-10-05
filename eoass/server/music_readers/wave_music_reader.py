from pathlib import Path
from typing import Text, Union
import wave

from .base_music_reader import BaseMusicReader

class WaveMusicReader(BaseMusicReader):
    def __init__(self, filepath: Union[Text, Path]) -> None:
        super().__init__()
        
        self._filepath = filepath
        if isinstance(filepath, Path):
            self._filepath = str(filepath)
        
        if not self._filepath.endswith('.wav') and not self._filepath.endswith('.wave'):
            raise Exception('File must be a wav file.')
            
        self._started = False
        self._current_position = 0
        self._opened_file: wave.Wave_read = None
        self._metadata = None
    
    @property
    def metadata(self) -> dict:
        if not self._metadata:
            wav_file = wave.open(self._filepath)
            self._metadata = dict()
            self._metadata["sample_width"] = wav_file.getsampwidth()
            self._metadata["channels"] = wav_file.getnchannels()
            self._metadata["framerate"] = wav_file.getframerate()
            wav_file.close()
        
        return self._metadata
    
    def read(self, music_time: int) -> bytes:
        """Reads the wav music file by the specified amount of time (in milliseconds).

        Args:
            music_time (int): The amount of time to read the file by (in milliseconds.)

        Returns:
            bytes: A chunk which contains data of the next `music_time` milliseconds of the file.
        """
        if self._finished:
            return b""
        
        if not self._started:
            self._opened_file = wave.open(self._filepath)
            self._started = True
            
        chunk = self._get_next_chunk(music_time)
        
        if self._opened_file.tell() == self._opened_file.getnframes():
            self._finished = True
            self._opened_file.close()
            
        return chunk
            
    def _get_frame_count_by_time(self, music_time: int):
        music_time_in_seconds = music_time / 1000
        return int(self._opened_file.getframerate() * music_time_in_seconds)
    
    def _get_next_chunk(self, music_time: int):
        return self._opened_file.readframes(self._get_frame_count_by_time(music_time))
    
    def __del__(self):
        if self._opened_file:
            self._opened_file.close()
            self._finished = True