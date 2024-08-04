import unittest
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.response_helper import get_plain_text_response
from skill import lambda_function

class TestSkill(unittest.TestCase):
    
    def setUp(self):
        """Set up the SkillBuilder and add handlers for testing."""
        self.sb = SkillBuilder()
        self.sb.add_request_handler(lambda_function.LaunchRequestHandler())
        self.sb.add_request_handler(lambda_function.LoopIntentHandler())
        self.sb.add_request_handler(lambda_function.StopIntentHandler())
        self.skill = self.sb.create()

    def _build_request(self, request_type, intent_name=None, slots=None):
        """Helper to build a mock request."""
        request = {
            "type": request_type,
            "requestId": "mockRequestId",
            "locale": "en-US"
        }

        if request_type == "IntentRequest" and intent_name:
            request["intent"] = {
                "name": intent_name,
                "slots": slots if slots else {}
            }

        return HandlerInput(request_envelope={
            "version": "1.0",
            "session": {
                "new": True,
                "sessionId": "mockSessionId",
                "application": {
                    "applicationId": "mockApplicationId"
                },
                "user": {
                    "userId": "mockUserId"
                }
            },
            "context": {
                "System": {
                    "application": {
                        "applicationId": "mockApplicationId"
                    },
                    "user": {
                        "userId": "mockUserId"
                    },
                    "device": {
                        "deviceId": "mockDeviceId"
                    },
                    "apiEndpoint": "https://api.amazonalexa.com"
                }
            },
            "request": request
        })

    def test_launch_request(self):
        """Test launch request when the skill is first invoked."""
        handler_input = self._build_request("LaunchRequest")
        response = self.skill.invoke(handler_input)
        self.assertIsNotNone(response)
        self.assertEqual(response.output_speech.ssml, get_plain_text_response("Welcome to the Sleep Loop. You can say 'Start Loop' to begin.").ssml)

    def test_loop_intent(self):
        """Test LoopIntent which should start the audio loop."""
        handler_input = self._build_request("IntentRequest", "LoopIntent")
        response = self.skill.invoke(handler_input)
        self.assertIsNotNone(response)
        self.assertIn("AudioPlayer.Play", response.directives[0].type)

    def test_stop_intent(self):
        """Test StopIntent which should stop the audio."""
        handler_input = self._build_request("IntentRequest", "AMAZON.StopIntent")
        response = self.skill.invoke(handler_input)
        self.assertIsNotNone(response)
        self.assertIn("AudioPlayer.Stop", response.directives[0].type)

if __name__ == '__main__':
    unittest.main()