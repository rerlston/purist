from typing import List
from unittest import TestCase

from errors import Error
from lexer import Lexer


class TestLexer(TestCase):
    def test_word_detection(self):
        # given
        text = "Hello other stuff"
        service = Lexer('test', text)

        # when
        word, error, line, column = service.next()

        # then
        self.assertEqual(word, 'Hello')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_positive_number_detection(self):
        # given
        text = "123 other stuff"
        service = Lexer('test', text)

        # when
        number, error, line, column = service.next()

        # then
        self.assertEqual(number, '123')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_negative_integer_detection(self):
        # given
        text = "-123 other stuff"
        service = Lexer('test', text)

        # when
        number, error, line, column = service.next()

        # then
        self.assertEqual(number, '-123')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_decimal_detection(self):
        # given
        text = "123.456 other stuff"
        service = Lexer('test', text)

        # when
        number, error, line, column = service.next()

        # then
        self.assertEqual(number, '123.456')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_negative_decimal_detection(self):
        # given
        text = "-123.456 other stuff"
        service = Lexer('test', text)

        # when
        number, error, line, column = service.next()

        # then
        self.assertEqual(number, '-123.456')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_detect_quoted_string(self):
        # given
        text = '"Hello" other stuff'
        service = Lexer('test', text)

        # when
        string, error, line, column = service.next()

        # then
        self.assertEqual(string, '"Hello"')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_detect_quoted_string_with_escaped_quote(self):
        # given
        text = '"This is an escaped quote\\" so string ends here" stuff'
        service = Lexer('test', text)

        # when
        string, error, line, column = service.next()

        # then
        self.assertEqual(string, '"This is an escaped quote\\" so string ends here"')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_detect_comment(self):
        # given
        text = '// Hello World'
        service = Lexer('test', text)

        # when
        comment, error, line, column = service.next()

        # then
        self.assertEqual(comment, '// Hello World')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_detect_comment2(self):
        # given
        text = '// Hello World\nnot a comment line'
        service = Lexer('test', text)

        # when
        comment, error, line, column = service.next()

        # then
        self.assertEqual(comment, '// Hello World')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_multi_line_string(self):
        # given
        text = '"Hello\nWorld"'
        service = Lexer('test', text)

        # when
        string, error, line, column = service.next()

        # then
        self.assertEqual(string, '"Hello\nWorld"')
        self.assertIsNone(error)
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_invalid_decimal(self):
        # given
        text = "123.456.789 other stuff"
        service = Lexer('test', text)

        # when
        value, error, line, column = service.next()

        # then
        self.assertIsNone(value)
        self.assertIsNotNone(error)
        if error is not None:
            value = 'Unexpected character: "too many decimal points" file: test, line: 1, column: 8'
            self.assertEqual(value, error.get_error())
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_decode_error(self):
        # given
        text = "$$$"
        service = Lexer('test', text)

        # when
        value, error, line, column = service.next()

        # then
        self.assertIsNone(value)
        self.assertIsNotNone(error)
        if error is not None:
            value = 'Unexpected character: "$" file: test, line: 1, column: 1'
            self.assertEqual(value, error.get_error())
        self.assertEqual(line, 1, 'line should be 1')
        self.assertEqual(column, 1, 'column should be 1')

    def test_multiline_simple_string_retrieve_multiple_entries(self):
        # given
        text = 'Hello\nWorld'
        service = Lexer('test', text)

        # when
        string1, error1, line1, column1 = service.next()
        string2, error2, line2, column2 = service.next()

        # then
        self.assertEqual(string1, 'Hello')
        self.assertIsNone(error1)
        self.assertEqual(line1, 1, 'line should be 1')
        self.assertEqual(column1, 1, 'column should be 1')
        self.assertEqual(string2, 'World')
        self.assertIsNone(error2)
        self.assertEqual(line2, 2, 'line should be 2')
        self.assertEqual(column2, 1, 'column should be 1')

    def test_multiline_string_with_items_in_square_brackets(self):
        # given
        text = 'from b require [B]\n\nclass A implements B{\n}'
        service = Lexer('test', text)

        # when
        strings: List[str|int|float|None] = []
        errors: List[Error|None] = []
        lines: List[int] = []
        columns: List[int] = []
        for index in range(12):
            string, error, line, column = service.next()
            strings.append(string)
            errors.append(error)
            lines.append(line)
            columns.append(column)

        # then
        # 'from'
        self.assertEqual(strings[0], 'from')
        self.assertIsNone(errors[0])
        self.assertEqual(lines[0], 1, 'line should be 1')
        self.assertEqual(columns[0], 1, 'column should be 1')

        # 'b'
        self.assertEqual(strings[1], 'b')
        self.assertIsNone(errors[1])
        self.assertEqual(lines[1], 1, 'line should be 1')
        self.assertEqual(columns[1], 6, 'column should be 6')

        # 'require'
        self.assertEqual(strings[2], 'require')
        self.assertIsNone(errors[2])
        self.assertEqual(lines[2], 1, 'line should be 1')
        self.assertEqual(columns[2], 8, 'column should be 8')

        # '['
        self.assertEqual(strings[3], '[')
        self.assertIsNone(errors[3])
        self.assertEqual(lines[3], 1, 'line should be 1')
        self.assertEqual(columns[3], 16, 'column should be 16')

        # 'B'
        self.assertEqual(strings[4], 'B')
        self.assertIsNone(errors[4])
        self.assertEqual(lines[4], 1, 'line should be 1')
        self.assertEqual(columns[4], 17, 'column should be 17')

        # ']'
        self.assertEqual(strings[5], ']')
        self.assertIsNone(errors[5])
        self.assertEqual(lines[5], 1, 'line should be 1')
        self.assertEqual(columns[5], 18, 'column should be 18')

        # 'class'
        self.assertEqual(strings[6], 'class')
        self.assertIsNone(errors[6])
        self.assertEqual(lines[6], 3, 'line should be 3')
        self.assertEqual(columns[6], 1, 'column should be 1')

        # 'A'
        self.assertEqual(strings[7], 'A')
        self.assertIsNone(errors[7])
        self.assertEqual(lines[7], 3, 'line should be 3')
        self.assertEqual(columns[7], 7, 'column should be 7')

        # 'implements'
        self.assertEqual(strings[8], 'implements')
        self.assertIsNone(errors[8])
        self.assertEqual(lines[8], 3, 'line should be 3')
        self.assertEqual(columns[8], 9, 'column should be 9')

        # 'B'
        self.assertEqual(strings[9], 'B')
        self.assertIsNone(errors[9])
        self.assertEqual(lines[9], 3, 'line should be 3')
        self.assertEqual(columns[9], 20, 'column should be 20')

        # '{'
        self.assertEqual(strings[10], '{')
        self.assertIsNone(errors[10])
        self.assertEqual(lines[10], 3, 'line should be 3')
        self.assertEqual(columns[10], 21, 'column should be 21')

        # '}''
        self.assertEqual(strings[11], '}')
        self.assertIsNone(errors[11])
        self.assertEqual(lines[11], 4, 'line should be 4')
        self.assertEqual(columns[11], 1, 'column should be 1')

    def test_comment(self):
        # given
        text = '// Hello World\nclass A {}'
        service = Lexer('test', text)

        # when
        strings: List[str|int|float|None] = []
        errors: List[Error|None] = []
        lines: List[int] = []
        columns: List[int] = []
        for index in range(5):
            string, error, line, column = service.next()
            strings.append(string)
            errors.append(error)
            lines.append(line)
            columns.append(column)

        # then
        # comment
        self.assertEqual(strings[0], '// Hello World')
        self.assertIsNone(errors[0])
        self.assertEqual(lines[0], 1, 'line should be 1')
        self.assertEqual(columns[0], 1, 'column should be 1')

        # 'class'
        self.assertEqual(strings[1], 'class')
        self.assertIsNone(errors[1])
        self.assertEqual(lines[1], 2, 'line should be 2')
        self.assertEqual(columns[1], 1, 'column should be 1')

        # 'A'
        self.assertEqual(strings[2], 'A')
        self.assertIsNone(errors[2])
        self.assertEqual(lines[2], 2, 'line should be 2')
        self.assertEqual(columns[2], 7, 'column should be 7')

        # '{'
        self.assertEqual(strings[3], '{')
        self.assertIsNone(errors[3])
        self.assertEqual(lines[3], 2, 'line should be 2')
        self.assertEqual(columns[3], 9, 'column should be 9')

        # '}'
        self.assertEqual(strings[4], '}')
        self.assertIsNone(errors[4])
        self.assertEqual(lines[4], 2, 'line should be 2')
        self.assertEqual(columns[4], 10, 'column should be 10')

    def test_multiline_code_with_commen(self):
        # given
        text = 'from b require [B]\n// comment\n\nclass A implements B{\n}'
        service = Lexer('test', text)

        # when
        strings: List[str|int|float|None] = []
        errors: List[Error|None] = []
        lines: List[int] = []
        columns: List[int] = []
        for index in range(13):
            string, error, line, column = service.next()
            strings.append(string)
            errors.append(error)
            lines.append(line)
            columns.append(column)

        # then
        # 'from'
        self.assertEqual(strings[0], 'from')
        self.assertIsNone(errors[0])
        self.assertEqual(lines[0], 1, 'line should be 1')
        self.assertEqual(columns[0], 1, 'column should be 1')

        # 'b'
        self.assertEqual(strings[1], 'b')
        self.assertIsNone(errors[1])
        self.assertEqual(lines[1], 1, 'line should be 1')
        self.assertEqual(columns[1], 6, 'column should be 6')
        # 'require'
        self.assertEqual(strings[2], 'require')
        self.assertIsNone(errors[2])
        self.assertEqual(lines[2], 1, 'line should be 1')
        self.assertEqual(columns[2], 8, 'column should be 8')

        # '['
        self.assertEqual(strings[3], '[')
        self.assertIsNone(errors[3])
        self.assertEqual(lines[3], 1, 'line should be 1')
        self.assertEqual(columns[3], 16, 'column should be 16')

        # 'B'
        self.assertEqual(strings[4], 'B')
        self.assertIsNone(errors[4])
        self.assertEqual(lines[4], 1, 'line should be 1')
        self.assertEqual(columns[4], 17, 'column should be 17')

        # ']'
        self.assertEqual(strings[5], ']')
        self.assertIsNone(errors[5])
        self.assertEqual(lines[5], 1, 'line should be 1')
        self.assertEqual(columns[5], 18, 'column should be 18')

        # 'comment'
        self.assertEqual(strings[6], '// comment')
        self.assertIsNone(errors[6])
        self.assertEqual(lines[6], 2, 'line should be 2')
        self.assertEqual(columns[6], 1, 'column should be 1')

        # 'class'
        self.assertEqual(strings[7], 'class')
        self.assertIsNone(errors[7])
        self.assertEqual(lines[7], 4, 'line should be 3')
        self.assertEqual(columns[7], 1, 'column should be 1')

        # 'A'
        self.assertEqual(strings[8], 'A')
        self.assertIsNone(errors[8])
        self.assertEqual(lines[8], 4, 'line should be 3')
        self.assertEqual(columns[8], 7, 'column should be 7')

        # 'implements'
        self.assertEqual(strings[9], 'implements')
        self.assertIsNone(errors[9])
        self.assertEqual(lines[9], 4, 'line should be 3')
        self.assertEqual(columns[9], 9, 'column should be 9')

        # 'B'
        self.assertEqual(strings[10], 'B')
        self.assertIsNone(errors[10])
        self.assertEqual(lines[10], 4, 'line should be 3')
        self.assertEqual(columns[10], 20, 'column should be 20')
