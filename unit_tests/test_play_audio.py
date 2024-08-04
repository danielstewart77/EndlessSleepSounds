import unittest
from unittest.mock import patch, MagicMock
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from skill.unit_tests.test_play_audio import play_audio_intent_handler


class TestPlayAudioIntent(unittest.TestCase):
    @patch('skill.unit_tests.test_play_audio.play_audio_intent_handler')
    def test_handler_response(self, mock_handler):
        """
        Test if the PlayAudioIntent handler returns the correct response.
        """
        handler_input = MagicMock(HandlerInput)
        handler_input.request_envelope.request.intent.name = 'PlayAudioIntent'
        expected_response = {
            "output_speech": "Audio is now playing.",
            "should_end_session": True
        }
        
        mock_handler.return_value = expected_response
        response = play_audio_intent_handler.handle(handler_input)
        
        # Assert that the handler returns the expected response
        self.assertEqual(response['output_speech'], expected_response['output_speech'])
        self.assertEqual(response['should_end_session'], expected_response['should_end_session'])

    def test_intent_name(self):
        """
        Test if the handler correctly identifies the PlayAudioIntent by name.
        """
        handler_input = MagicMock(HandlerInput)
        handler_input.request_envelope.request.intent.name = 'PlayAudioIntent'
        
        # Assert that is_intent_name identifies the intent correctly
        self.assertTrue(is_intent_name('PlayAudioIntent')(handler_input))
        
        # Changing intent name for negative test
        handler_input.request_envelope.request.intent.name = 'OtherIntent'
        self.assertFalse(is_intent_name('PlayAudioIntent')(handler_input))

if __name__ == '__main__':
    unittest.main()
