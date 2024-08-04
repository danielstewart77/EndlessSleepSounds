import unittest
from skill.handlers import StopAudioIntentHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from unittest.mock import MagicMock, patch

class TestStopAudioIntentHandler(unittest.TestCase):
    def setUp(self):
        # Set up mock for HandlerInput
        self.handler_input = MagicMock(spec=HandlerInput)
        self.handler_input.request_envelope.request.intent.name = "AMAZON.StopIntent"

        self.stop_audio_intent_handler = StopAudioIntentHandler()

    def test_can_handle_stop_intent(self):
        # Test that the StopAudioIntentHandler can handle the StopIntent
        self.assertTrue(self.stop_audio_intent_handler.can_handle(self.handler_input))

    @patch('skill.handlers.ResponseFactory.speak')
    @patch('skill.handlers.ResponseFactory.response')
    def test_handle_stop_intent(self, mock_response, mock_speak):
        # Mock the speak and response methods
        mock_speak.return_value = "Audio stopped"
        mock_response.return_value = {}

        # Call the handle method
        response = self.stop_audio_intent_handler.handle(self.handler_input)

        # Check that the speak method was called with "Audio stopped"
        mock_speak.assert_called_once_with("Audio stopped")

        # Check that the response method was called
        mock_response.assert_called_once()

        # Ensure the response returned by handle method is as expected
        self.assertEqual(response, {})

if __name__ == '__main__':
    unittest.main()