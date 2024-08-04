# Import necessary modules from the ask-sdk-core and ask-sdk-model packages
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_model import Response

# Initialize the SkillBuilder instance
sb = SkillBuilder()

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch"""
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "LaunchRequest"

    def handle(self, handler_input):
        speech_text = "Welcome to the Sleep Loop skill. I will loop an audio file for you all night." 
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

class PlayAudioIntentHandler(AbstractRequestHandler):
    """Handler for Play Audio Intent"""
    def can_handle(self, handler_input):
        return is_intent_name("PlayAudioIntent")(handler_input)

    def handle(self, handler_input):
        audio_url = "https://example.com/path_to_audio_file.mp3"
        return handler_input.response_builder.speak("Playing your looping audio now.").add_directive({
            'type': 'AudioPlayer.Play',
            'playBehavior': 'REPLACE_ALL',
            'audioItem': {
                'stream': {
                    'token': 'looping-audio',
                    'url': audio_url,
                    'offsetInMilliseconds': 0,
                    'expectedPreviousToken': None
                }
            }
        }).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End"""
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "SessionEndedRequest"

    def handle(self, handler_input):
        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """Reflects the intent back to the user"""
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "IntentRequest"

    def handle(self, handler_input):
        intent_name = handler_input.request_envelope.request.intent.name
        speech_text = "You just triggered " + intent_name
        return handler_input.response_builder.speak(speech_text).response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Custom global exception handler to catch all exceptions"""
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        return handler_input.response_builder.speak("Sorry, I didn't catch that. Can you please repeat?").ask("Can you please repeat?").response

# Add all request handlers and exception handlers to the SkillBuilder instance
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PlayAudioIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

# Lambda handler to be used in AWS Lambda
lambda_handler = sb.lambda_handler()