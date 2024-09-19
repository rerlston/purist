from unittest import TestCase

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
