import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.interfaces.audioplayer import StopDirective

logger = logging.getLogger(__name__)

class StopAudioIntentHandler(AbstractRequestHandler):
    """
    Handler for StopAudioIntent which stops the audio loop.
    """

    def can_handle(self, handler_input: HandlerInput) -> bool:
        """
        Check if the handler can handle the incoming request based on the intent name.

        Parameters:
        handler_input (HandlerInput): The input from Alexa Skill request.

        Returns:
        bool: True if the incoming request is StopAudioIntent, False otherwise.
        """
        return handler_input.request_envelope.request.intent.name == "StopAudioIntent"

    def handle(self, handler_input: HandlerInput) -> Response:
        """
        Handle the StopAudioIntent by sending a StopDirective to stop the audio loop.

        Parameters:
        handler_input (HandlerInput): The input from Alexa Skill request.

        Returns:
        Response: The response to be sent back to Alexa.
        """
        logger.info("In StopAudioIntentHandler")

        # Create a StopDirective to signal Alexa to stop the current audio playback
        stop_audio_directive = StopDirective()

        return handler_input.response_builder.add_directive(stop_audio_directive).speak("Stopping the audio.").response
