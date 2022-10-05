from abc import ABC, abstractmethod, abstractproperty


class BaseMusicReader(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._finished = False
        
    @property
    def finished(self) -> bool:
        return self._finished
    
    @property
    @abstractmethod
    def metadata(self) -> dict:
        ...
        
    @abstractmethod
    def read(self, music_time: int) -> bytes:
        """Reads the wav music file by the specified amount of time (in milliseconds).

        Args:
            music_time (int): The amount of time to read the file by (in milliseconds.)

        Returns:
            bytes: A chunk which contains data of the next `music_time` milliseconds of the file.
        """
        ...
