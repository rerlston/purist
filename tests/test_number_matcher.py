from unittest import TestCase
from unittest.mock import MagicMock

from purist.lexer.number_matcher import NumberMatcher
from purist.models.lexer_models import LexerResult, LexerType
from purist.utils.logger import Logger, LogLevel


class TestBracketMatcher(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.INFO)
        self._mocked_state = MagicMock()

    def test_have_number(self):
        # given
        self._mocked_state.next_character.side_effect = [
            ("1", False),
            ("2", False),
            ("3", False),
            ("4", False),
            ("5", False),
            ("6", False),
            ("7", False),
            ("8", False),
            ("9", False),
            ("0", False),
            (" ", False),
        ]
        self._mocked_state.peek_next_character.return_value = "2", False
        service = NumberMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NUMBER_LITERAL)
        self.assertEqual(result.value, "1234567890")
        self._mocked_state.next_character.assert_called()

    def test_have_number_at_end_of_line(self):
        # given
        self._mocked_state.next_character.side_effect = [
            ("1", False),
            ("2", False),
            ("3", False),
            ("4", False),
            ("5", False),
            ("6", False),
            ("7", False),
            ("8", False),
            ("9", False),
            ("0", True),
        ]
        self._mocked_state.peek_next_character.return_value = "2", False
        service = NumberMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NUMBER_LITERAL)
        self.assertEqual(result.value, "1234567890")
        self._mocked_state.next_character.assert_called()

    def test_have_float(self):
        # given
        self._mocked_state.next_character.side_effect = [
            ("1", False),
            ("2", False),
            ("3", False),
            (".", False),
            ("4", False),
            ("5", False),
            ("6", False),
            ("7", False),
            ("8", False),
            ("9", False),
            ("0", False),
            (" ", False),
        ]
        self._mocked_state.peek_next_character.return_value = "2", False
        service = NumberMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.FLOAT_LITERAL)
        self.assertEqual(result.value, "123.4567890")
        self._mocked_state.next_character.assert_called()
