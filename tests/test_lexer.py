from typing import List
from unittest import TestCase

from purist.lexer import Lexer
from purist.models.lexer_models import LexerResult, LexerType
from purist.utils.errors import Error


class TestLexer(TestCase):
    def test_semantic_equals_comparitor(self):
        # given
        text = "=="
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.CALCULATION_LOGIC)
        self.assertEqual(result.value, "==")

    def test_semantic_not_equals_comparitor(self):
        # given
        text = "!="
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.CALCULATION_LOGIC)
        self.assertEqual(result.value, "!=")

    def test_number(self):
        # given
        text = "1234"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NUMBER)
        self.assertEqual(result.value, "1234")

    def test_semantic_subtract_comparitor(self):
        # given
        text = "10 - 3"
        service = Lexer("test", text)
        service.next()

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.CALCULATION_LOGIC)
        self.assertEqual(result.value, "-")

    def test_semantic_add_comparitor(self):
        # given
        text = "3+5"
        service = Lexer("test", text)
        service.next()  # move past the number

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.CALCULATION_LOGIC)
        self.assertEqual(result.value, "+")

    def test_semantic_multiply_comparitor(self):
        # given
        text = "5* 6"
        service = Lexer("test", text)
        service.next()  # skip over first toke (numbr)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.CALCULATION_LOGIC)
        self.assertEqual(result.value, "*")

    def test_semantic_mod_comparitor(self):
        # given
        text = "1 %2"
        service = Lexer("test", text)
        service.next()

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.CALCULATION_LOGIC)
        self.assertEqual(result.value, "%")

    def test_semantic_not_comparitor(self):
        # given
        text = "a = !b"
        service = Lexer("test", text)
        service.next()  # skip over identifier
        service.next()  # skip over operator

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.CALCULATION_LOGIC)
        self.assertEqual(result.value, "!")

    def test_semantic_opening_round_bracket(self):
        # given
        text = "("
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GRAMMAR_STRUCTURE)
        self.assertEqual(result.value, "(")

    def test_semantic_closing_round_bracket(self):
        # given
        text = ")"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GRAMMAR_STRUCTURE)
        self.assertEqual(result.value, ")")

    def test_semantic_opening_curly_bracket(self):
        # given
        text = "{"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GRAMMAR_STRUCTURE)
        self.assertEqual(result.value, "{")

    def test_semantic_closing_curly_bracket(self):
        # given
        text = "}"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GRAMMAR_STRUCTURE)
        self.assertEqual(result.value, "}")

    def test_semantic_opening_square_bracket(self):
        # given
        text = "["
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GRAMMAR_STRUCTURE)
        self.assertEqual(result.value, "[")

    def test_semantic_closing_square_bracket(self):
        # given
        text = "]"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GRAMMAR_STRUCTURE)
        self.assertEqual(result.value, "]")

    def test_semantic_colon(self):
        # given
        text = "name: type"
        service = Lexer("test", text)
        service.next()

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.META_LANGUAGE)
        self.assertEqual(result.value, ":")

    def test_semantic_assign(self):
        # given
        text = "a = b"
        service = Lexer("test", text)
        service.next()

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.META_LANGUAGE)
        self.assertEqual(result.value, "=")

    def test_semantic_fullstop(self):
        # given
        text = "a.b"
        service = Lexer("test", text)
        service.next()

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.META_LANGUAGE)
        self.assertEqual(result.value, ".")

    def test_word_detection(self):
        # given
        text = "Hello other stuff"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertEqual(result.type, LexerType.IDENTIFIER)
        self.assertEqual(result.value, "Hello")
        state = result.state
        self.assertEqual(state.line, 0, "line should be 0")
        self.assertEqual(state.column, 6, "column should be 0")

    def test_positive_number_detection(self):
        # given
        text = "123 other stuff"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NUMBER)
        self.assertEqual(result.value, "123")

    def test_negative_integer_detection(self):
        # given
        text = "-123 other stuff"
        service = Lexer("test", text)

        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NUMBER)
        self.assertEqual(result.value, "-123")

    def test_decimal_detection(self):
        # given
        text = "123.456 other stuff"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NUMBER)
        self.assertEqual(result.value, "123.456")

    def test_negative_decimal_detection(self):
        # given
        text = "-123.456 other stuff"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NUMBER)
        self.assertEqual(result.value, "-123.456")

    def test_detect_quoted_string(self):
        # given
        text = '"Hello" other stuff'
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertEqual(result.value, '"Hello"')
        self.assertEqual(result.type, LexerType.STRING)

    def test_detect_quoted_string_with_escaped_quote(self):
        # given
        text = 'quoted "this is the quoted string" other stuff'
        service = Lexer("test", text)
        service.next()

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.STRING)
        self.assertEqual(result.value, '"this is the quoted string"')

    def test_semantic_divide_comparitor(self):
        # given
        text = "1 / 2"
        service = Lexer("test", text)
        service.next()

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.CALCULATION_LOGIC)
        self.assertEqual(result.value, "/")

    def test_detect_comment(self):
        # given
        text = "// Hello World"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertEqual(result.type, LexerType.COMMENT)
        self.assertEqual(result.value, "// Hello World")

    def test_detect_comment_after_identifier(self):
        # given
        text = "identifier // comment"
        service = Lexer("test", text)
        service.next()

        # when
        result = service.next()

        # then
        self.assertEqual(result.type, LexerType.COMMENT)
        self.assertEqual(result.value, "// comment")

    def test_detect_comment2(self):
        # given
        text = "// Hello World\nnot a comment line"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertEqual(result.type, LexerType.COMMENT)
        self.assertEqual(result.value, "// Hello World")

    def test_multi_line_string(self):
        # given
        text = '"Hello\nWorld"'
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertEqual(result.type, LexerType.STRING)
        self.assertEqual(result.value, '"Hello\nWorld"')

    def test_invalid_decimal(self):
        # given
        text = "123.456.789 other stuff"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Error)
        self.assertEqual(
            result.error,
            "Invalid Syntax Error: 123.456.789 other stu file: test, line: 1, column: 1\r\n                      ^",
        )

    def test_decode_error(self):
        # given
        text = "$$$"
        service = Lexer("test", text)

        # when
        result = service.next()

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Error)
        self.assertEqual(
            result.error,
            "Invalid Syntax Error: $$ file: test, line: 1, column: 1\r\n                      ^",
        )
