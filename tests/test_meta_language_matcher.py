from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock

from purist.lexer.operation_meta_language_matcher import OperationMetaLanguageMatcher
from purist.models.lexer_models import LexerResult, TokenType
from purist.utils.logger import Logger, LogLevel


class TestMetaLanguageMatcher(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.INFO)

        self._mocked_state = MagicMock()

        self._mocked_previous_result = MagicMock()

    def test_fullstop(self):
        # given
        text = "."
        self._mocked_state.next_character.return_value = text, False
        service = OperationMetaLanguageMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.PERIOD)
        self.assertEqual(result.value, ".")
        self._mocked_state.next_character.assert_called_once()

    def test_no_result(self):
        # given
        text = "N/A"
        self._mocked_state.next_character.return_value = text, False
        service = OperationMetaLanguageMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)
        self._mocked_state.next_character.assert_called_once()

    def test_unusable_previous(self):
        # given
        text = "N/A"
        self._mocked_state.next_character.return_value = text, False
        service = OperationMetaLanguageMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)
        self._mocked_state.next_character.assert_called_once()

    def test_next_char_is_on_new_line(self):
        # given
        text = ":"
        self._mocked_state.next_character.return_value = text, True
        service = OperationMetaLanguageMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)
        self._mocked_state.next_character.assert_called_once()
