from pathlib import Path
from typing import List, Text

from ....music_readers.wave_music_reader import WaveMusicReader


class LocalFileSystemMusicStorage:
    def __init__(self, root: Path) -> None:
        self._root = root
        
    def get_music_reader(self, filename: str):
        for file in self._root.iterdir():
            without_suffix = "".join(file.name.split('.')[:-1])
            if filename.lower() == without_suffix.lower():
                return WaveMusicReader(file.absolute())
            
        return None
    
    def get_all(self) -> List[Text]:
        r = []
        for file in self._root.iterdir():
            without_suffix = "".join(file.name.split('.')[:-1])
            r.append(without_suffix)
        return r