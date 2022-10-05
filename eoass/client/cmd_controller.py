from eoass.client.handlers.music_player import MusicPlayer
from eoass.message_types import MessageType
from .eoass_client import EOASSClient


class CMDContoller:
    def __init__(self, eoass_client: EOASSClient, player: MusicPlayer) -> None:
        self._client = eoass_client
        self._welcome_message = None
        self._running = False
        self._player = player
        
    def start(self):
        self._client.start()
        self._running = True
        
        response = self._client.send_command({"Type": MessageType.Welcome})
        print(response["welcome_message"])
        print('To start listening to a song, simply tap on the number. To resume/pause, type `resume` or `pause`.')
        print('To exit, type `exit`.')
        print('-' * 30)
        
        # for i, room in enumerate(response["rooms"]):
        #     requires_password = "YES" if room["requires_password"] else "NO"
        #     print(f'{i + 1}. {room["name"]} - HOSTED BY {room["owner"]} - REQUIRES PASSWORD: {requires_password}')
        
        files = response["files"]
        for i, file in enumerate(files):
            print(f'{i + 1}. {file}')
            
        print('-' * 30)
                
        while self._running:
            user_input = input('FILE TO PLAY >>> ').lower()
            
            if user_input.isnumeric() and int(user_input) <= len(files):
                data = {
                    "Type": MessageType.ChangeMusicFile,
                    "file_name": files[int(user_input) - 1]
                }
                self._player.clean()
                self._client.send_command(data)
                # Immediately request the server to start streaming the file
                self._client.send_command({ "Type": MessageType.MusicStreamContinue }, False)
                
            elif user_input == 'pause':
                self._player.pause()
            elif user_input == 'resume':
                self._player.resume()
            elif user_input == 'exit':
                self._running = False
                
            