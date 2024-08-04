import logging
import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.interfaces.audioplayer import PlayDirective, PlayBehavior, AudioItem, Stream

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Skill Builder instance
sb = SkillBuilder()

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "LaunchRequest"

    def handle(self, handler_input):
        logger.info("In LaunchRequestHandler")
        speech_text = "Welcome to the Sleep Sound Skill. Let me play some soothing sounds to help you sleep."

        return (
            handler_input.response_builder
                .speak(speech_text)
                .set_card(SimpleCard("Sleep Sound", speech_text))
                .add_directive(self.play_audio())
                .response
        )

    @staticmethod
    def play_audio():
        return PlayDirective(
            play_behavior=PlayBehavior.REPLACE_ALL,
            audio_item=AudioItem(
                stream=Stream(
                    token="1",
                    url="https://sparktobloom.com/rain/rain_light.mp3",
                    offset_in_milliseconds=0,
                    expected_previous_token=None
                )
            )
        )

class ErrorHandler(AbstractExceptionHandler):
    """Handler for catching exceptions."""
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speech_text = "Sorry, I couldn't understand the command. Please try again."

        return (
            handler_input.response_builder
                .speak(speech_text)
                .set_card(SimpleCard("Error", speech_text))
                .response
        )

# Registering handlers to the skill builder
sb.add_request_handler(LaunchRequestHandler())
sb.add_exception_handler(ErrorHandler())

# Handler name that will be invoked by the Lambda runtime
lambda_handler = sb.lambda_handler()
