from enum import Enum
from typing import Tuple

from purist.utils.logger import Logger


class LexerState:
    def __init__(self, filepath: str, text: str) -> None:
        self._filepath = filepath
        self._text = text
        self._line = 0
        self._column = 0
        lines = text.splitlines()
        self._lines = [line.rstrip() for line in lines]
        self._saved_column = 0
        self._saved_line = 0
        Logger.info(lines[0])

    def saveState(self) -> None:
        self._saved_column = self._column
        self._saved_line = self._line

    def restoreState(self) -> None:
        self._column = self._saved_column
        self._line = self._saved_line

    def next_character(self) -> Tuple(str | None, bool):
        new_line = False
        if self._line >= len(self._lines):
            return None, True
        if self._column >= len(self._lines[self._line]):
            return None, True
        character = self._lines[self._line][self._column]
        self._column = self._column + 1
        if self._column > len(self._lines[self._line]):
            new_line = True
            self._column = 0
            self._line = self._line + 1
            if self._line > len(self._lines):
                return None, True
            Logger.info(self._lines[self._line])
        return character, new_line

    def get_line(self) -> int | None:
        return self._line

    def get_column(self) -> int | None:
        return self._column


class LexerType(Enum):
    STRING = "string"
    COMMENT = "comment"
    CALCULATION_LOGIC = "comparison"
    GRAMMAR_STRUCTURE = "grouping"
    META_LANGUAGE = "operator"
    NUMBER = "number"
    RESERVED_WORD = "word"
    UNKNOWN = "unknown"


class LexerResult:
    def __init__(
        self, lexer_type: LexerType, value: str | None, state: LexerState
    ) -> None:
        self._lexer_type = lexer_type
        self._value = value
        self._state = state

    def get_value(self) -> str | None:
        return self._value

    def get_type(self) -> LexerType:
        return self._lexer_type

    def get_state(self) -> LexerState:
        return self._state
