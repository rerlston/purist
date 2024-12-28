"""
Purist Lexer, converts discovered source code values into tokens
"""

from typing import List

from purist.lexer import Lexer
from purist.models.token import Token, TokenType

class Tokenizer():
    """
    Purist Tokenizer, converts discovered source code values into tokens
    """
    def tokenize(self, filepath: str, text: str) -> List[Token]:
        """
        Converts discovered source code values into tokens

        Args:
            filepath (str): The source code filepath
            text (str): The source code text

        Returns:
            List[Token]: The list of tokens
        """
        response: List[Token] = []
        lexer: Lexer = Lexer(filepath, text)
        next_value, error, line, column = lexer.next()
        while next_value is not None and error is None:
            if next_value == 'from':
                response.append(Token(TokenType.FROM, filepath, line, column, next_value))
            elif next_value == 'Builtin':
                response.append(Token(TokenType.BUILTIN, filepath, line, column, next_value))
            elif next_value == 'require':
                response.append(Token(TokenType.REQUIRE, filepath, line, column, next_value))
            elif next_value == 'class':
                response.append(Token(TokenType.CLASS, filepath, line, column, next_value))
            elif next_value == 'interface':
                response.append(Token(TokenType.INTERFACE, filepath, line, column, next_value))
            elif next_value == 'type':
                response.append(Token(TokenType.TYPE, filepath, line, column, next_value))
            elif next_value == 'enumeration':
                response.append(Token(TokenType.ENUMERATION, filepath, line, column, next_value))
            elif next_value == 'extends':
                response.append(Token(TokenType.EXTENDS, filepath, line, column, next_value))
            elif next_value == 'implements':
                response.append(Token(TokenType.IMPLEMENTS, filepath, line, column, next_value))
            elif next_value == 'string':
                response.append(Token(TokenType.STRING_TYPE, filepath, line, column, next_value))
            elif next_value == 'boolean':
                response.append(Token(TokenType.BOOLEAN_TYPE, filepath, line, column, next_value))
            elif next_value == 'integer':
                response.append(Token(TokenType.INTEGER_TYPE, filepath, line, column, next_value))
            elif next_value == 'number':
                response.append(Token(TokenType.DECIMAL_TYPE, filepath, line, column, next_value))
            elif next_value == 'false' or next_value == 'true':
                response.append(Token(TokenType.BOOLEAN_VALUE, filepath, line, column, next_value))
            elif next_value == 'null':
                response.append(Token(TokenType.NULL, filepath, line, column, next_value))
            elif next_value.startswith('"'):
                response.append(Token(TokenType.STRING_VALUE, filepath, line, column, next_value))
            elif next_value == ',':
                response.append(Token(TokenType.COMMA, filepath, line, column, next_value))
            elif next_value == 'private':
                response.append(Token(TokenType.PRIVATE, filepath, line, column, next_value))
            elif next_value == 'public':
                response.append(Token(TokenType.PUBLIC, filepath, line, column, next_value))
            elif next_value == '[':
                response.append(Token(TokenType.LEFT_SQUARE_BRACKET, filepath, line, column, next_value))
            elif next_value == ']':
                response.append(Token(TokenType.RIGHT_SQUARE_BRACKET, filepath, line, column, next_value))
            elif next_value == '(':
                response.append(Token(TokenType.LEFT_BRACKET, filepath, line, column, next_value))
            elif next_value == ')':
                response.append(Token(TokenType.RIGHT_BRACKET, filepath, line, column, next_value))
            elif next_value == '{':
                response.append(Token(TokenType.LEFT_CURLY_BRACKET, filepath, line, column, next_value))
            elif next_value == '}':
                response.append(Token(TokenType.RIGHT_CURLY_BRACKET, filepath, line, column, next_value))
            elif next_value == ':':
                response.append(Token(TokenType.COLON, filepath, line, column, next_value))
            elif next_value == '=':
                response.append(Token(TokenType.EQUALS, filepath, line, column, next_value))
            elif next_value == '<':
                response.append(Token(TokenType.LEFT_ANGLE_BRACKET, filepath, line, column, next_value))
            elif next_value == '>':
                response.append(Token(TokenType.RIGHT_ANGLE_BRACKET, filepath, line, column, next_value))
            elif next_value == '.':
                response.append(Token(TokenType.FULL_STOP, filepath, line, column, next_value))
            elif next_value == '!':
                response.append(Token(TokenType.NOT, filepath, line, column, next_value))
            elif next_value == 'constructor':
                response.append(Token(TokenType.CONSTRUCTOR, filepath, line, column, next_value))
            elif next_value == 'destructor':
                response.append(Token(TokenType.DESTRUCTOR, filepath, line, column, next_value))
            elif next_value == '|':
                response.append(Token(TokenType.LOGICAL_OR, filepath, line, column, next_value))
            elif next_value.startswith('//'):
                response.append(Token(TokenType.COMMENT, filepath, line, column, next_value))
            elif self._is_integer(next_value):
                response.append(
                    Token(TokenType.INTEGER_VALUE, filepath, line, column, int(next_value))
                )
            elif self._is_float(next_value) and next_value.count('.') == 1:
                response.append(
                    Token(TokenType.DECIMAL_VALUE, filepath, line, column, float(next_value))
                )
            else:
                response.append(Token(TokenType.IDENTIFIER, filepath, line, column, next_value))
            next_value, error, line, column = lexer.next()
        if error is not None:
            raise ValueError(error.get_error())

        response.append(Token(TokenType.EOF, filepath, line, 0))
        return response

    def _is_float(self, value: str) -> bool:
        if value[0] not in ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return False
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _is_integer(self, value: str) -> bool:
        if value[0] not in ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return False
        try:
            int(value)
            return True
        except ValueError:
            return False
