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
        self.assertIsNotNone(token.value)

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
        self.assertIsNotNone(token.value)
        self.assertEqual('from', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.BUILTIN, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('Builtin', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.REQUIRE, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('require', token.value)
        token = tokens[3]
        self.assertEqual(TokenType.LEFT_SQUARE_BRACKET, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('[', token.value)
        token = tokens[4]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('ABC', token.value)
        token = tokens[5]
        self.assertEqual(TokenType.RIGHT_SQUARE_BRACKET, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual(']', token.value)
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
        self.assertIsNotNone(token.value)
        self.assertEqual('from', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('sample', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.FULL_STOP, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('.', token.value)
        token = tokens[3]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('package', token.value)
        token = tokens[4]
        self.assertEqual(TokenType.REQUIRE, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('require', token.value)
        token = tokens[5]
        self.assertEqual(TokenType.LEFT_SQUARE_BRACKET, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('[', token.value)
        token = tokens[6]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('ABC', token.value)
        token = tokens[7]
        self.assertEqual(TokenType.RIGHT_SQUARE_BRACKET, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual(']', token.value)
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
        self.assertIsNotNone(token.value)
        self.assertEqual('class', token.value)
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
        self.assertIsNotNone(token.value)
        self.assertEqual('class', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.EXTENDS, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('extends', token.value)
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
        self.assertIsNotNone(token.value)
        self.assertEqual('class', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.IMPLEMENTS, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('implements', token.value)
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
        self.assertIsNotNone(token.value)
        self.assertEqual('class', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.IMPLEMENTS, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('implements', token.value)
        token = tokens[3]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Base', token.value)
        token = tokens[4]
        self.assertEqual(TokenType.COMMA, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual(',', token.value)
        token = tokens[5]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Other', token.value)
        token = tokens[6]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_class_with_empty_class_definition(self):
        # given
        tokenizer = Tokenizer()
        code = 'class Test {\n}'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(5, len(tokens))
        token = tokens[0]
        self.assertEqual(TokenType.CLASS, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('class', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.LEFT_CURLY_BRACKET, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('{', token.value)
        token = tokens[3]
        self.assertEqual(TokenType.RIGHT_CURLY_BRACKET, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('}', token.value)
        token = tokens[4]
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
        self.assertIsNotNone(token.value)
        self.assertEqual('interface', token.value)
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
        self.assertIsNotNone(token.value)
        self.assertEqual('interface', token.value)
        token = tokens[1]
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('Test', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.EXTENDS, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('extends', token.value)
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
        self.assertIsNotNone(token.value)
        self.assertEqual('type', token.value)
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
        self.assertIsNotNone(token.value)
        self.assertEqual('enumeration', token.value)
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
        self.assertIsNotNone(token.value)
        self.assertEqual(':', token.value)
        token = tokens[2]
        self.assertEqual(TokenType.INTEGER_TYPE, token.type)
        self.assertIsNotNone(token.value)
        self.assertEqual('integer', token.value)
        token = tokens[3]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)

    def test_multiline_code_to_tokens(self):
        # given
        tokenizer = Tokenizer()
        code = 'from b require [B]\n\nclass A implements B{\n}'

        # when
        tokens = tokenizer.tokenize('unittest', code)

        # then
        self.assertIsNotNone(tokens)
        self.assertEqual(13, len(tokens))
        token = tokens[0]
        # 'from'
        self.assertEqual(TokenType.FROM, token.type)
        self.assertEqual(1, token.line)
        self.assertEqual(1, token.column)
        token = tokens[1]
        # 'b'
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('b', token.value)
        self.assertEqual(1, token.line)
        self.assertEqual(6, token.column)
        token = tokens[2]
        # 'require
        self.assertEqual(TokenType.REQUIRE, token.type)
        self.assertEqual(1, token.line)
        self.assertEqual(8, token.column)
        token = tokens[3]
        # '['
        self.assertEqual(TokenType.LEFT_SQUARE_BRACKET, token.type)
        self.assertEqual(1, token.line)
        self.assertEqual(16, token.column)
        token = tokens[4]
        # 'B'
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('B', token.value)
        self.assertEqual(1, token.line)
        self.assertEqual(17, token.column)
        token = tokens[5]
        # ']'
        self.assertEqual(TokenType.RIGHT_SQUARE_BRACKET, token.type)
        self.assertEqual(1, token.line)
        self.assertEqual(18, token.column)
        token = tokens[6]
        # 'class'
        self.assertEqual(TokenType.CLASS, token.type)
        self.assertEqual(3, token.line)
        self.assertEqual(1, token.column)
        token = tokens[7]
        # 'A'
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('A', token.value)
        self.assertEqual(3, token.line)
        self.assertEqual(7, token.column)
        token = tokens[8]
        # 'implements'
        self.assertEqual(TokenType.IMPLEMENTS, token.type)
        self.assertEqual(3, token.line)
        self.assertEqual(9, token.column)
        token = tokens[9]
        # 'B'
        self.assertEqual(TokenType.IDENTIFIER, token.type)
        self.assertEqual('B', token.value)
        self.assertEqual(3, token.line)
        self.assertEqual(20, token.column)
        token = tokens[10]
        # '{'
        self.assertEqual(TokenType.LEFT_CURLY_BRACKET, token.type)
        self.assertEqual(3, token.line)
        self.assertEqual(21, token.column)
        token = tokens[11]
        # '}'
        self.assertEqual(TokenType.RIGHT_CURLY_BRACKET, token.type)
        self.assertEqual(4, token.line)
        self.assertEqual(1, token.column)
        token = tokens[12]
        self.assertEqual(TokenType.EOF, token.type)
        self.assertIsNone(token.value)
