from typing import List
from unittest import TestCase

from purist.lexer.tokenizer import Tokenizer
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.errors import Error
from purist.utils.logger import Logger, LogLevel


class TestLexer(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.DEBUG)

    def test_single_letter_string(self):
        # given
        # a = b + c, return a as a character
        pass

    def test_word_as_string(self):
        # given
        # myVariable = 1
        pass

    def test_skip_spaces(self):
        # given
        text = "service Abc123{ constructor() "
        #       012345678901234567890123456789
        service = LexerState("test", text)
        service.skip_spaces()  # should be at 0 still
        self.assertEqual(service.column, 0)
        for a in range(1, 8):
            service.next_character()
        # should be at first space
        self.assertEqual(service.column, 7)

        # when
        service.skip_spaces()  # should be at A of Abc123

        # then
        self.assertEqual(service.column, 8)
