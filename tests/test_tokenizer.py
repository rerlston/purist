from unittest import TestCase
from unittest.mock import MagicMock

from purist.lexer.tokenizer import Tokenizer
from purist.models.lexer_models import LexerResult, TokenType, LexerState
from purist.utils.errors import InvalidSyntaxError
from purist.utils.logger import Logger, LogLevel


class TestTokenizer(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.INFO)
        self._mocked_state = MagicMock()

    def test_eof(self):
        # given
        self._mocked_state.return_value.is_eof.return_value = True
        matchers = []
        service = Tokenizer(matchers, self._mocked_state)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.EOF)

    def test_second_eof(self):
        # given
        self._mocked_state.is_eof.side_effect = [False, True]
        matchers = []
        service = Tokenizer(matchers, self._mocked_state)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.EOF)

    def test_find_largest_matcher(self):
        # given
        self._mocked_state.is_eof.return_value = False
        matchers = []
        mocked_matcher = MagicMock()
        mocked_matcher.try_match.return_value = LexerResult(
            TokenType.ADDITION, "+", self._mocked_state
        )
        matchers.append(mocked_matcher)
        service = Tokenizer(matchers, self._mocked_state)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.ADDITION)

    def test_find_largest_matcher_fails_with_syntax_error(self):
        # given
        self._mocked_state.is_eof.return_value = False
        matchers = []
        service = Tokenizer(matchers, self._mocked_state)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, InvalidSyntaxError)

    def test_list_tokens(self):
        # given
        text = """
        service Abc123{
            constructor(){}
            public void method(){}
        }"""
        state = LexerState("test", text)
        service = Tokenizer(Tokenizer.setup(), state)

        # when
        service_token = service.next()
        identifier_token_1 = service.next()
        left_curly_token_1 = service.next()
        constructor_token = service.next()
        left_round_token_1 = service.next()
        right_round_token_1 = service.next()
        left_curly_token_2 = service.next()
        right_curly_token_1 = service.next()
        public_token = service.next()
        void_token = service.next()
        identifier_token_2 = service.next()
        left_round_token_2 = service.next()
        right_round_token_2 = service.next()
        left_curly_token_3 = service.next()
        right_curly_token_2 = service.next()
        right_curly_token_3 = service.next()

        # then
        # service
        self.assertIsInstance(service_token, LexerResult)
        self.assertEqual(service_token.type, TokenType.SERVICE)

        # Abc123
        self.assertIsInstance(identifier_token_1, LexerResult)
        self.assertEqual(identifier_token_1.type, TokenType.IDENTIFIER)

        # { 1
        self.assertIsInstance(left_curly_token_1, LexerResult)
        self.assertEqual(left_curly_token_1.type, TokenType.L_CURLY)

        # constructor
        self.assertIsInstance(constructor_token, LexerResult)
        self.assertEqual(constructor_token.type, TokenType.CONSTRUCTOR)

        # ( 1
        self.assertIsInstance(left_round_token_1, LexerResult)
        self.assertEqual(left_round_token_1.type, TokenType.L_ROUND)

        # ) 1
        self.assertIsInstance(right_round_token_1, LexerResult)
        self.assertEqual(right_round_token_1.type, TokenType.R_ROUND)

        # { 2
        self.assertIsInstance(left_curly_token_2, LexerResult)
        self.assertEqual(left_curly_token_2.type, TokenType.L_CURLY)

        # } 2
        self.assertIsInstance(right_curly_token_1, LexerResult)
        self.assertEqual(right_curly_token_1.type, TokenType.R_CURLY)

        # public
        self.assertIsInstance(public_token, LexerResult)
        self.assertEqual(public_token.type, TokenType.PUBLIC)

        # void
        self.assertIsInstance(void_token, LexerResult)
        self.assertEqual(void_token.type, TokenType.VOID)

        # method
        self.assertIsInstance(identifier_token_2, LexerResult)
        self.assertEqual(identifier_token_2.type, TokenType.IDENTIFIER)

        # ( 2
        self.assertIsInstance(left_round_token_2, LexerResult)
        self.assertEqual(left_round_token_2.type, TokenType.L_ROUND)

        # ) 2
        self.assertIsInstance(right_round_token_2, LexerResult)
        self.assertEqual(right_round_token_2.type, TokenType.R_ROUND)

        # { 3
        self.assertIsInstance(left_curly_token_3, LexerResult)
        self.assertEqual(left_curly_token_3.type, TokenType.L_CURLY)

        # } 2
        self.assertIsInstance(right_curly_token_2, LexerResult)
        self.assertEqual(right_curly_token_2.type, TokenType.R_CURLY)

        # } 3
        self.assertIsInstance(right_curly_token_3, LexerResult)
        self.assertEqual(right_curly_token_3.type, TokenType.R_CURLY)

        service.next()

    def test_test_first_character(self):
        # given
        text = """
        // this is a simple class extending another class

class AnotherClass {
    // no defined methods
}

class SimpleClass extends AnotherClass {
}
        """
        state = LexerState("test", text)
        service = Tokenizer(Tokenizer.setup(), state)

        # when
        service.next()
        class_token = service.next()
        Logger.trace(class_token)

        # then
        self.assertIsInstance(class_token, LexerResult)
        self.assertEqual(class_token.type, TokenType.SERVICE)
