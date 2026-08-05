import copy

from enum import Enum
from typing import Self, Tuple

from purist.utils.logger import Logger


class LexerState:

    def __init__(self, filepath: str, text: str) -> None:
        self._filepath = filepath
        self._text = text
        self._line = 0
        self._column = 0
        lines = text.splitlines()
        self._lines = [line.rstrip() for line in lines]
        self.__set_peekable()

    def __set_peekable(self):
        max_peek = len(self._lines[self._line]) - self._column
        self._peekable = 0
        if max_peek >= 0:
            if max_peek > 20:
                self._peekable = self._lines[self._line][
                    self._column - 1 : self._column + 20
                ]
            else:
                self._peekable = self._lines[self._line][self._column :]

    def next_character(self) -> Tuple(str | None, bool):
        new_line = False
        if self._column >= len(self._lines[self._line]):
            self._line += 1
            self._column = 0
            new_line = True
        if self._line >= len(self._lines):
            return None, True
        # Logger.info(
        #     f"line {self._line + 1} of {len(self._lines)}, column {self._column + 1} of {len(self._lines[self._line])}"
        # )
        character = self._lines[self._line][self._column]
        self._column = self._column + 1
        if self._column > len(self._lines[self._line]):
            new_line = True
            self._column = 0
            self._line = self._line + 1
            if self._line > len(self._lines):
                return None, True
            Logger.info(self._lines[self._line])
        self.__set_peekable()
        return character, new_line

    def step_back(self) -> None:
        if self._column > 0:
            self._column = self._column - 1
        else:
            self._line = self.line - 1
            self._column = len(self._lines[self._line]) - 1
        self.__set_peekable()

    @property
    def line(self) -> int | None:
        return self._line

    @property
    def column(self) -> int | None:
        return self._column

    @property
    def filename(self) -> str | None:
        return self._filepath

    def set_new_state(self, new_column: int, new_line: int) -> bool:
        is_new_line = False
        if new_line < len(self._lines):
            self._line = new_line
        if new_column < len(self._lines[self._line]):
            self._column = new_column
            is_new_line = False
        else:
            self._column = 0
            new_line = True
        self.__set_peekable()
        return is_new_line

    def peek(self) -> str:
        return self._peekable

    def clone(self) -> Self:
        return copy.copy(self)

    def __copy__(self):
        new_clone = self.__class__.__new__(self.__class__)
        new_clone.__dict__.update(self.__dict__)
        return new_clone


class LexerType(Enum):
    STRING = "string"
    COMMENT = "comment"
    UNARY_LOGIC = "unary"
    BINARY_LOGIC = "binary"
    TERNARY_LOGIC = "ternary"
    GRAMMAR_STRUCTURE = "grouping"
    NUMBER = "number"
    RESERVED_WORD = "word"
    IDENTIFIER = "identifier"
    CONSTANT = "constant"
    PASCAL_CASE = "pascal"
    UNKNOWN = "unknown"


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
