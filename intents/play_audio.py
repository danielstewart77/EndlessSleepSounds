import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response
from ask_sdk_model.interfaces.audioplayer import PlayDirective, PlayBehavior, AudioItem, Stream

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# This class handles the PlayAudioIntent
class PlayAudioIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Check if the incoming request is PlayAudioIntent
        return is_intent_name('PlayAudioIntent')(handler_input)

    def handle(self, handler_input):
        # Log the intent handling
        logger.info('In PlayAudioIntentHandler')

        # URL to the audio file to be played
        audio_url = 'https://sparktobloom.com/rain/rain_light.mp3'
        
        # Creating the stream object for the audio item
        stream = Stream(
            token='unique-token',
            url=audio_url,
            offset_in_milliseconds=0
        )

        # Creating the audio item object
        audio_item = AudioItem(
            stream=stream
        )

        # Creating the play directive object
        play_directive = PlayDirective(
            play_behavior=PlayBehavior.REPLACE_ALL,
            audio_item=audio_item
        )

        # Creating and returning the response with the play directive
        return handler_input.response_builder.add_directive(play_directive).response
