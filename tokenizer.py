"""
Purist Lexer, converts discovered source code values into tokens
"""

from enum import Enum
from typing import List

from lexer import Lexer

class TokenType(Enum):
    """
    Purist Token Types
    """

    CLASS = 'CLASS'
    INTERFACE = 'INTERFACE'
    TYPE = 'TYPE'
    ENUMERATION = 'ENUMERATION'
    EXTENDS = 'EXTENDS'
    IMPLEMENTS = 'IMPLEMENTS'
    FROM = 'FROM'
    BUILTIN = 'BUILTIN'
    REQUIRE = 'REQUIRE'
    IDENTIFIER = 'IDENTIFIER'
    INTEGER_TYPE = 'INTEGER_TYPE'
    INTEGER_VALUE = 'INTEGER_VALUE'
    NUMBER_TYPE = 'NUMBER_TYPE'
    NUMBER_VALUE = 'NUMBER_VALUE'
    STRING_TYPE = 'STRING_TYPE'
    STRING_VALUE = 'STRING_VALUE'
    BOOLEAN_TYPE = 'BOOLEAN_TYPE'
    BOOLEAN_VALUE = 'BOOLEAN_VALUE'
    LEFT_SQUARE_BRACKET = 'LEFT_SQUARE_BRACKET'
    RIGHT_SQUARE_BRACKET = 'RIGHT_SQUARE_BRACKET'
    LEFT_BRACKET = 'LEFT_BRACKET'
    RIGHT_BRACKET = 'RIGHT_BRACKET'
    LEFT_CURLY_BRACKET = 'LEFT_CURLY_BRACKET'
    RIGHT_CURLY_BRACKET = 'RIGHT_CURLY_BRACKET'
    LEFT_ANGLE_BRACKET = 'LEFT_ANGLE_BRACKET'
    RIGHT_ANGLE_BRACKET = 'RIGHT_ANGLE_BRACKET'
    COMMA = 'COMMA'
    PRIVATE = 'PRIVATE'
    PUBLIC = 'PUBLIC'
    CLASS_BODY = 'CLASS_BODY'
    INTERFACE_BODY = 'INTERFACE_BODY'
    TYPE_BODY = 'TYPE_BODY'
    ENUMERATION_BODY = 'ENUMERATION_BODY'
    GENERIC_TYPE = 'GENERIC_TYPE'
    CLASS_IDENTIFIER = 'CLASS_IDENTIFIER'
    INTERFACE_IDENTIFIER = 'INTERFACE_IDENTIFIER'
    TYPE_IDENTIFIER = 'TYPE_IDENTIFIER'
    ENUMERATION_IDENTIFIER = 'ENUMERATION_IDENTIFIER'
    VARIABLE = 'VARIABLE'
    CONSTANT = 'CONSTANT'
    NEW = 'NEW'
    WHILE = 'WHILE'
    IF = 'IF'
    ELSE = 'ELSE'
    RETURN = 'RETURN'
    FOR = 'FOR'
    IN = 'IN'
    COLON = 'COLON'
    EQUALS = 'EQUALS'
    FULL_STOP = 'FULL_STOP'
    NOT = 'NOT'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    NULL = 'NULL'
    LOGICAL_OR = 'LOGICAL_OR'
    COMMENT = 'COMMENT'
    EOF = "EOF"

class Token():
    """
    Purist Token, simple model class representing the parsers tokens
    """
    def __init__(
            self,
            type: TokenType,
            filename: str,
            line: int,
            column: int,
            value: str|int|float|None = None
    ) -> None:
        self._type = type
        self._filename = filename
        self._line = line
        self._column = column
        self._value = value

    @property
    def type(self) -> TokenType:
        return self._type

    @property
    def value(self) -> str|int|float|None:
        return self._value

    def __repr__(self) -> str:
        print(self._type)
        if self._value is not None:
            return f'({str(self._type)} = {self._value})'
        else:
            return f'({str(self._type)})'

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def line(self) -> int:
        return self._line

    @property
    def column(self) -> int:
        return self._column

class Tokenizer():
    """
    Purist Tokenizer, converts discovered source code values into tokens
    """
    def __init__(self) -> None:
        pass

    def tokenize(self, filepath: str, text: str) -> List[Token]:
        response: List[Token] = []
        lexer: Lexer = Lexer(filepath, text)
        next_value, error, line, column = lexer.next()
        while next_value is not None and error is None:
            if next_value == 'from':
                response.append(Token(TokenType.FROM, filepath, line, column))
            elif next_value == 'Builtin':
                response.append(Token(TokenType.BUILTIN, filepath, line, column))
            elif next_value == 'require':
                response.append(Token(TokenType.REQUIRE, filepath, line, column))
            elif next_value == 'class':
                response.append(Token(TokenType.CLASS, filepath, line, column))
            elif next_value == 'interface':
                response.append(Token(TokenType.INTERFACE, filepath, line, column))
            elif next_value == 'type':
                response.append(Token(TokenType.TYPE, filepath, line, column))
            elif next_value == 'enumeration':
                response.append(Token(TokenType.ENUMERATION, filepath, line, column))
            elif next_value == 'extends':
                response.append(Token(TokenType.EXTENDS, filepath, line, column))
            elif next_value == 'implements':
                response.append(Token(TokenType.IMPLEMENTS, filepath, line, column))
            elif next_value == 'string':
                response.append(Token(TokenType.STRING_TYPE, filepath, line, column))
            elif next_value == 'boolean':
                response.append(Token(TokenType.BOOLEAN_TYPE, filepath, line, column))
            elif next_value == 'integer':
                response.append(Token(TokenType.INTEGER_TYPE, filepath, line, column))
            elif next_value == 'number':
                response.append(Token(TokenType.NUMBER_TYPE, filepath, line, column))
            elif next_value == 'false' or next_value == 'true':
                response.append(Token(TokenType.BOOLEAN_VALUE, filepath, line, column, next_value))
            elif next_value == 'null':
                response.append(Token(TokenType.NULL, filepath, line, column))
            elif next_value.isnumeric() and '.' not in next_value:
                response.append(Token(TokenType.INTEGER_VALUE, filepath, line, column, next_value))
            elif next_value.isnumeric():
                response.append(Token(TokenType.NUMBER_VALUE, filepath, line, column, next_value))
            elif next_value.startswith('"'):
                response.append(Token(TokenType.STRING_VALUE, filepath, line, column, next_value))
            elif next_value == ',':
                response.append(Token(TokenType.COMMA, filepath, line, column))
            elif next_value == '[':
                response.append(Token(TokenType.LEFT_SQUARE_BRACKET, filepath, line, column))
            elif next_value == ']':
                response.append(Token(TokenType.RIGHT_SQUARE_BRACKET, filepath, line, column))
            elif next_value == '(':
                response.append(Token(TokenType.LEFT_BRACKET, filepath, line, column))
            elif next_value == ')':
                response.append(Token(TokenType.RIGHT_BRACKET, filepath, line, column))
            elif next_value == '{':
                response.append(Token(TokenType.LEFT_CURLY_BRACKET, filepath, line, column))
            elif next_value == '}':
                response.append(Token(TokenType.RIGHT_CURLY_BRACKET, filepath, line, column))
            elif next_value == ':':
                response.append(Token(TokenType.COLON, filepath, line, column))
            elif next_value == '=':
                response.append(Token(TokenType.EQUALS, filepath, line, column))
            elif next_value == '<':
                response.append(Token(TokenType.LEFT_ANGLE_BRACKET, filepath, line, column))
            elif next_value == '>':
                response.append(Token(TokenType.RIGHT_ANGLE_BRACKET, filepath, line, column))
            elif next_value == '.':
                response.append(Token(TokenType.FULL_STOP, filepath, line, column))
            elif next_value == '!':
                response.append(Token(TokenType.NOT, filepath, line, column))
            elif next_value == '|':
                response.append(Token(TokenType.LOGICAL_OR, filepath, line, column))
            elif next_value.startswith('//'):
                response.append(Token(TokenType.COMMENT, filepath, line, column))
            else:
                response.append(Token(TokenType.IDENTIFIER, filepath, line, column, next_value))
            next_value, error, line, column = lexer.next()
        if error is not None:
            print(error.get_error())
            return []

        response.append(Token(TokenType.EOF, filepath, line, 0))
        return response
