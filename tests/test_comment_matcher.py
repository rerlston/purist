from unittest import TestCase
from unittest.mock import MagicMock

from purist.lexer.comment_matcher import CommentMatcher
from purist.models.lexer_models import LexerResult, TokenType
from purist.utils.logger import Logger, LogLevel


class TestCommentMatcher(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.INFO)
        self._mocked_state = MagicMock()

    def test_have_comment(self):
        # given
        self._mocked_state.next_character.side_effect = [
            ("/", False),
            ("/", False),
            (" ", False),
            ("c", False),
            ("o", False),
            ("m", False),
            ("m", False),
            ("e", False),
            ("n", False),
            ("t", False),
            ("", True),
        ]
        self._mocked_state.peek_next_character.return_value = "/", False
        service = CommentMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.COMMENT)
        self.assertEqual(result.value, "// comment")
        self._mocked_state.next_character.assert_called()

    def test_no_comment_found(self):
        # given
        self._mocked_state.next_character.side_effect = [
            ("#", False),
            (" ", False),
            ("c", False),
            ("o", False),
            ("m", False),
            ("m", False),
            ("e", False),
            ("n", False),
            ("t", False),
            ("", True),
        ]
        self._mocked_state.peek_next_character.return_value = "#", False
        service = CommentMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

    def test_have_divide(self):
        # given
        self._mocked_state.next_character.side_effect = [
            ("/", False),
            ("1", False),
            ("", True),
        ]
        self._mocked_state.peek_next_character.return_value = "1", False
        service = CommentMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)
