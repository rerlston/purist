from unittest import TestCase

from tokenizer import TokenType, Tokenizer


class TestTokenizer(TestCase):
    def test_identifier_as_token(self):
        # given
        tokenizer = Tokenizer()

        # when
        tokens = tokenizer.tokenize('unittest', 'word')

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(2, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('word', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_number_as_token(self):
        # given
        tokenizer = Tokenizer()

        # when
        tokens = tokenizer.tokenize('unittest', '123')

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(2, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.INTEGER_VALUE, token.type)
        self.assertEqual(123, token.value)
        token = tokens[1]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_negative_number_as_token(self):
        # given
        tokenizer = Tokenizer()

        # when
        tokens = tokenizer.tokenize('unittest', '-123')

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(2, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.INTEGER_VALUE, token.type)
        self.assertEqual(-123, token.value)
        token = tokens[1]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_string_as_token(self):
        # given
        tokenizer = Tokenizer()

        # when
        tokens = tokenizer.tokenize('unittest', '"hello"')

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(2, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.STRING_VALUE, token.type)
        self.assertEqual('"hello"', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_keyword_as_token(self):
        # given
        tokenizer = Tokenizer()

        # when
        tokens = tokenizer.tokenize('unittest', 'true')

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(2, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.BOOLEAN_VALUE, token.type)
        self.assertEqual('true', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_decimal_as_token(self):
        # given
        tokenizer = Tokenizer()

        # when
        tokens = tokenizer.tokenize('unittest', '1.2')

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(2, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.DECIMAL_VALUE, token.type)
        self.assertEqual(1.2, token.value)
        token = tokens[1]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_negative_decimal_as_token(self):
        # given
        tokenizer = Tokenizer()

        # when
        tokens = tokenizer.tokenize('unittest', '-1.2')

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(2, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.DECIMAL_VALUE, token.type)
        self.assertEqual(-1.2, token.value)
        token = tokens[1]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_comment_as_token(self):
        # given
        tokenizer = Tokenizer()

        # when
        tokens = tokenizer.tokenize('unittest', '// this is a comment')

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(2, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.COMMENT, token.type)
        self.assertIsNone(token.value)

    def test_builtin_import_as_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'from Builtin require [ABC]'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(7, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.FROM, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.BUILTIN, token.type)
        self.assertIsNone(token.value)
        token = tokens[2]
        self.assertEqual(TokenType.REQUIRE, token.type)
        self.assertIsNone(token.value)
        token = tokens[3]
        self.assertEqual(TokenType.LEFT_SQUARE_BRACKET, token.type)
        self.assertIsNone(token.value)
        token = tokens[4]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('ABC', token.value)
        token = tokens[5]
        self.assertEqual(TokenType.RIGHT_SQUARE_BRACKET, token.type)
        self.assertIsNone(token.value)
        token = tokens[6]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_custom_import_as_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'from sample.package require [ABC]'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(9, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.FROM, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('sample', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.FULL_STOP, token.type)
        self.assertIsNone(token.value)
        token = tokens[3]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('package', token.value)
        token = tokens[4]
        self.assertEqual(TokenType.REQUIRE, token.type)
        self.assertIsNone(token.value)
        token = tokens[5]
        self.assertEqual(TokenType.LEFT_SQUARE_BRACKET, token.type)
        self.assertIsNone(token.value)
        token = tokens[6]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('ABC', token.value)
        token = tokens[7]
        self.assertEqual(TokenType.RIGHT_SQUARE_BRACKET, token.type)
        self.assertIsNone(token.value)
        token = tokens[8]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_simple_class_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'class Test'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(3, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.CLASS, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_class_with_extends_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'class Test extends Base'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(5, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.CLASS, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.EXTENDS, token.type)
        self.assertIsNone(token.value)
        token = tokens[3]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Base', token.value)
        token = tokens[4]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_class_with_single_implements_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'class Test implements Base'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(5, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.CLASS, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.IMPLEMENTS, token.type)
        self.assertIsNone(token.value)
        token = tokens[3]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Base', token.value)
        token = tokens[4]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_class_with_multiple_implements_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'class Test implements Base, Other'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(7, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.CLASS, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.IMPLEMENTS, token.type)
        self.assertIsNone(token.value)
        token = tokens[3]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Base', token.value)
        token = tokens[4]
        self.assertEqual(TokenType.COMMA, token.type)
        self.assertIsNone(token.value)
        token = tokens[5]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Other', token.value)
        token = tokens[6]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_interface_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'interface Test'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(3, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.INTERFACE, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_interface_with_extends_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'interface Test extends Base'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(5, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.INTERFACE, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.EXTENDS, token.type)
        self.assertIsNone(token.value)
        token = tokens[3]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Base', token.value)
        token = tokens[4]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_type_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'type Test'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(3, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.TYPE, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_enumeration_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'enumeration Test'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(3, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.ENUMERATION, token.type)
        self.assertIsNone(token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_integer_variable_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'test:integer'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(4, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('test', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.COLON, token.type)
        self.assertIsNone(token.value)
        token = tokens[2]
        self.assertEqual(TokenType.INTEGER_TYPE, token.type)
        self.assertIsNone(token.value)
        token = tokens[3]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)
