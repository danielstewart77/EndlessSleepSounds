import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize a SkillBuilder instance
sb = SkillBuilder()

# Handler for the launch request
class LaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch.
    """
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return handler_input.request_envelope.request.type == "LaunchRequest"

    def handle(self, handler_input: HandlerInput) -> Response:
        speech_text = "Welcome to the Sleep Loop Skill. Say 'start sleep loop' to begin playing the audio."
        return (
            handler_input.response_builder
                .speak(speech_text)
                .reprompt(speech_text)
                .get_response()
        )

# Handler to start the sleep loop
class StartSleepLoopIntentHandler(AbstractRequestHandler):
    """
    Handler for Start Sleep Loop Intent.
    """
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return handler_input.request_envelope.request.intent.name == "StartSleepLoopIntent"

    def handle(self, handler_input: HandlerInput) -> Response:
        # URL of the audio file to loop
        audio_url = "https://sparktobloom/rain/rain_light.mp3"
        speech_text = (
            f"Starting the sleep loop. Say 'stop sleep loop' to stop the audio."
        )
        # Constructing the audio response
        return (
            handler_input.response_builder
                .speak(speech_text)
                .add_directive({
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": "1",
                            "url": audio_url,
                            "offsetInMilliseconds": 0
                        }
                    }
                })
                .get_response()
        )

# Handler to stop the sleep loop
class StopSleepLoopIntentHandler(AbstractRequestHandler):
    """
    Handler for Stop Sleep Loop Intent.
    """
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return handler_input.request_envelope.request.intent.name == "StopSleepLoopIntent"

    def handle(self, handler_input: HandlerInput) -> Response:
        speech_text = "Stopping the sleep loop."
        return (
            handler_input.response_builder
                .speak(speech_text)
                .add_directive({
                    "type": "AudioPlayer.Stop"
                })
                .get_response()
        )

#Handle intent or request that Alexa does not know how to handle
class FallbackIntentHandler(AbstractRequestHandler):
    """
    Handler for Fallback Intent.
    """
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return handler_input.request_envelope.request.intent.name == "AMAZON.FallbackIntent"

    def handle(self, handler_input: HandlerInput) -> Response:
        speech_text = "Sorry, I don't know that one. You can say 'start sleep loop' to begin playing the audio."
        return (
            handler_input.response_builder
                .speak(speech_text)
                .reprompt(speech_text)
                .get_response()
        )

# Error Handler
class ErrorHandler(AbstractRequestHandler):
    """
    Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input: HandlerInput, exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception) -> Response:
        logger.error(exception, exc_info=True)
        speech_text = "Sorry, I couldn't understand what you said. Please try again."
        return (
            handler_input.response_builder
                .speak(speech_text)
                .reprompt(speech_text)
                .get_response()
        )

# Register the request handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StartSleepLoopIntentHandler())
sb.add_request_handler(StopSleepLoopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())

# Register the error handler
sb.add_exception_handler(ErrorHandler())

# Lambda handler entry point
lambda_handler = sb.lambda_handler()
