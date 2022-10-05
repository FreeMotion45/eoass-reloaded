from eoass.client.cmd_controller import CMDContoller
from eoass.client.eoass_client import EOASSClient
from eoass.client.handlers.music_data_handler import MusicDataHandler
from eoass.client.handlers.music_player import MusicPlayer
from eoass.message_types import MessageType
from eoass.protocol import SimpleProtocol
from eoass.serialization.eoass_pre_post_serialization_processor import EOASSPrePostSerializationProcessor
from eoass.serialization.serializer import JsonSerializer

player = MusicPlayer()
client = EOASSClient("127.0.0.1", SimpleProtocol(JsonSerializer(), EOASSPrePostSerializationProcessor()), player)
cmd_controller = CMDContoller(client, player)
cmd_controller.start()