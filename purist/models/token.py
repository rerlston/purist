from enum import Enum

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
    DECIMAL_TYPE = 'NUMBER_TYPE'
    DECIMAL_VALUE = 'DECIMAL_VALUE'
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
    CONSTRUCTOR = 'CONSTRUCTOR'
    DESTRUCTOR = 'DESTRUCTOR'
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
    URL = 'URL'
    VOID = 'VOID'
    EOF = "EOF"

class Token():
    """
    Purist Token, simple model class representing the parsers tokens
    """
    def __init__(
            self,
            token_type: TokenType,
            filename: str,
            line: int,
            column: int,
            value: str|int|float|None = None
    ) -> None:
        self._type = token_type
        self._filename = filename
        self._line = line
        self._column = column
        self._value = value

    @property
    def type(self) -> TokenType:
        """
        Returns the type of the token

        Returns:
            TokenType: The type of the token
        """
        return self._type

    @property
    def value(self) -> str|int|float|None:
        """
        Returns the value of the token

        Returns:
            str|int|float|None: The value of the token
        """
        return self._value

    @property
    def filename(self) -> str:
        """
        Returns the filename where the token was derived

        Returns:
            str: The filename where the token was discovered
        """
        return self._filename

    @property
    def line(self) -> int:
        """
        Returns the line number where the token was derived

        Returns:
            int: The line number where the token was discovered
        """
        return self._line

    @property
    def column(self) -> int:
        """
        Returns the column number where the token was derived

        Returns:
            int: The column number where the token was discovered
        """
        return self._column

    def __repr__(self) -> str:
        if self._value is not None:
            if self._type == TokenType.IDENTIFIER or self._type == TokenType.STRING_VALUE or self._type == TokenType.INTEGER_VALUE or self._type == TokenType.DECIMAL_VALUE:
                return f'({self._type.__repr__()}[{self._line}:{self._column}] = \'{self._value}\')\n'
            return f'({self._type.__repr__()}[{self._line}:{self._column}])\n'
        else:
            return f'({self._type.__repr__()}[{self._line}:{self._column}])\n'
