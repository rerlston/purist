import copy

from enum import IntEnum
from typing import Self, Tuple

from purist.utils.logger import Logger


class LexerState:

    def __init__(self, filepath: str, text: str) -> None:
        self._filepath = filepath
        self._text = text
        self._start_line = 0
        self._start_column = 0
        self._current_line = 0
        self._current_column = 0
        lines = text.splitlines()
        self._lines = [line.rstrip() for line in lines]
        self._lines = [line for line in self._lines if line]
        self._reached_eof = False

    def _check_if_next_line(self):
        is_new_line = False
        if self._current_line >= len(self._lines):
            self._reached_eof = True
            return True
        if self._current_column >= len(self._lines[self._current_line]):
            self._current_line += 1
            self._current_column = 0
            is_new_line = True
            if self._current_line >= len(self._lines):
                self._reached_eof = True
        else:
            Logger.trace(
                f"{self._current_line}/{len(self._lines)}:{self._current_column}/{len(self._lines[self._current_line])}"
            )
        return is_new_line

    def next_character(self) -> Tuple[str | None, bool]:
        is_new_line = self._check_if_next_line()
        if not self._reached_eof:
            character = self._lines[self._current_line][self._current_column]
            Logger.trace(f"{character}:{is_new_line}")
            self._current_column = self._current_column + 1
            return character, is_new_line
        return None, True

    def peek_next_character(self) -> Tuple[str | None, bool]:
        current_line = self._current_line
        current_column = self._current_column
        peeked, new_line = self.next_character()
        self._current_column = current_column
        self._current_line = current_line
        return peeked, new_line

    def consume(self):
        self._start_line = self._current_line
        self._start_column = self._current_column
        self._check_if_next_line()

    def is_eof(self) -> bool:
        return self._reached_eof

    def skip_spaces(self):
        if (
            self._current_line < len(self._lines)
            and len(self._lines[self._current_line]) > 0
        ):
            Logger.trace(
                f"skip_spaces: {self._current_column}[{self._lines[self._current_line][self._current_column]}]"
            )
            next_character = self._lines[self._current_line][self._current_column]
            new_line = False
            while next_character in [" ", "\t"] and not new_line:
                next_character, new_line = self.next_character()
                next_character, new_line = self.peek_next_character()
            Logger.trace(
                f"skip_spaces: {self._current_column}[{self._lines[self._current_line][self._current_column]}]"
            )

    def clone(self) -> Self:
        return copy.deepcopy(self)

    @property
    def line(self) -> int | None:
        return self._current_line

    @property
    def column(self) -> int | None:
        return self._current_column

    @property
    def start_column(self) -> int:
        return self.start_column

    @property
    def start_line(self) -> int:
        return self._start_line

    @property
    def filename(self) -> str | None:
        return self._filepath

    def __str__(self) -> str:
        output = f"(LexerState: {self._start_line}:{self._start_column})\r\n{self._lines[self._start_line]}"
        filler = "-" * (self._start_column)
        filler = f"{filler}^"
        output = f"{output}\r\n{filler}"
        return output


class LexerType(IntEnum):
    STRING_LITERAL = 0
    COMMENT = 1
    LOGICAL_NOT = 2
    STRING_CONCATENATION = 3
    L_ROUND = 4
    R_ROUND = 5
    L_SQUARE = 6
    R_SQUARE = 7
    L_CURLY = 8
    R_CURLY = 9
    L_ANGLE = 10
    R_ANGLE = 11
    NUMBER_LITERAL = 12
    TRUE = 13
    FALSE = 14
    NONE = 15
    NULL = 16
    IDENTIFIER = 17
    CONSTANT = 18
    SERVICE = 19
    INTENT = 20
    MODEL = 21
    FULFILLS = 22
    BEHAVES_LIKE = 23
    BLUEPRINT = 24
    ENUMERATION = 25
    INCREMENT = 26
    DECREMENT = 27
    NEGATION = 28
    ADDITION = 29
    SUBTRACTION = 30
    MOD = 31
    XOR = 32
    DIVIDE = 33
    MULTIPLY = 34
    POWER = 35
    EQUALS = 36
    ASSIGN = 37
    NOT_EQUALS = 38
    GREATER_OR_EQUAL = 39
    GREATER_THAN = 40
    LESS_OR_EQUAL = 41
    LESS_THAN = 42
    LOGICAL_OR = 43
    MATH_OR = 44
    LOGICAL_AND = 45
    MATH_AND = 46
    QUESTION = 47
    PERIOD = 48
    COLON = 49
    DEFINITION = 50
    VOID = 51
    IN = 52
    FOR = 53
    RETURN = 54
    ELSE = 55
    IF = 56
    WHILE = 57
    NEW = 58
    CONSTRUCTOR = 59
    DESTRUCTOR = 60
    COMMA = 61
    PRIVATE = 62
    PUBLIC = 63
    FLOAT_LITERAL = 64
    IS = 65
    THIS = 66
    VIRTUAL = 67
    IMPORT = 69
    FROM = 69
    REQUIRE = 70
    FLOAT_TYPE = 71
    STRING_TYPE = 72
    BOOL_TYPE = 73
    NUMBER_TYPE = 74
    AT = 75
    PATH_SEPARATOR = 76
    DATE_TYPE = 77
    SUPER = 78

    EOF = 99
    UNKNOWN = 100

    def __str__(self) -> str:
        output = f"LexerType<{self.name}>"
        return output


class LexerResult:
    def __init__(
        self, lexer_type: LexerType, value: str | None, state: LexerState
    ) -> None:
        self._lexer_type = lexer_type
        self._value = value
        self._state = state

    @property
    def value(self) -> str | None:
        return self._value

    @property
    def type(self) -> LexerType:
        return self._lexer_type

    @property
    def state(self) -> LexerState:
        return self._state

    def __str__(self) -> str:
        output = f'LexerResult<{self._lexer_type}:"{self.value}">{self.state}'
        return output
