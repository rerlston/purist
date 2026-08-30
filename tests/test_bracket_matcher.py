from unittest import TestCase
from unittest.mock import MagicMock

from purist.lexer.operation_bracket_matcher import OperationBracketMatcher
from purist.models.lexer_models import LexerResult, LexerType
from purist.utils.logger import Logger, LogLevel


class TestBracketMatcher(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.INFO)
        self._mocked_state = MagicMock()

    def test_open_round_bracket(self):
        # given
        text = "("
        self._mocked_state.next_character.return_value = text, False
        service = OperationBracketMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.L_ROUND)
        self.assertEqual(result.value, "(")
        self._mocked_state.next_character.assert_called()

    def test_close_round_bracket(self):
        # given
        text = ")"
        self._mocked_state.next_character.return_value = text, False
        service = OperationBracketMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.R_ROUND)
        self.assertEqual(result.value, ")")
        self._mocked_state.next_character.assert_called()

    def test_open_square_bracket(self):
        # given
        text = "["
        self._mocked_state.next_character.return_value = text, False
        service = OperationBracketMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.L_SQUARE)
        self.assertEqual(result.value, "[")
        self._mocked_state.next_character.assert_called()

    def test_close_square_bracket(self):
        # given
        text = "]"
        self._mocked_state.next_character.return_value = text, False
        service = OperationBracketMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.R_SQUARE)
        self.assertEqual(result.value, "]")
        self._mocked_state.next_character.assert_called()

    def test_open_curly_bracket(self):
        # given
        text = "{"
        self._mocked_state.next_character.return_value = text, False
        service = OperationBracketMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.L_CURLY)
        self.assertEqual(result.value, "{")
        self._mocked_state.next_character.assert_called()

    def test_close_curly_bracket(self):
        # given
        text = "}"
        self._mocked_state.next_character.return_value = text, False
        service = OperationBracketMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.R_CURLY)
        self.assertEqual(result.value, "}")
        self._mocked_state.next_character.assert_called()

    def test_no_bracket_found(self):
        # given
        text = "--"
        self._mocked_state.next_character.return_value = text, False
        service = OperationBracketMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)
        self._mocked_state.next_character.assert_called()
