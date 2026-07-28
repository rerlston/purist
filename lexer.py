"""
Purist source code lexer, reads source code and discovers words, numbers, operators, etc
"""

from typing import Tuple

from utils.errors import DecodeError, Error
from utils.logger import Logger

VALID_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890"


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

    def saveState(self) -> None:
        self._saved_column = self._column
        self._saved_line = self._line

    def restoreState(self) -> None:
        self._column = self._saved_column
        self._line = self._saved_line

    def next_character(self) -> str | None:
        character = self._lines[self._line][self._column]
        self._column = self._column + 1
        if self._column >= len(self._lines[self._line]):
            self._column = 0
            self._line = self._line + 1
            if self._line > len(self._lines):
                return None
        return character


class LexerResult:
    def __init__(self, value: str, state: LexerState) -> None:
        self._value = value
        self._state = state

    def get_value(self) -> str | None:
        return self._value


class Matcher(ABC):
    def __init__(self):
        self._next_matcher = None

    def set_next(self, matcher):
        self._next_matcher = matcher
        return matcher

    @abstractmethod
    def try_match(self, state: LexerState) -> LexerResult | Error:
        if self._next_matcher:
            return self._next_matcher.try_match(state)
        return Error(
            "Unrecognised character",
            "Unparsable",
            state._filepath,
            state._line,
            state._column,
        )


class OperationMatcher(Matcher):
    def try_match(self, state: LexerState) -> LexerResult | Error:
        return super().try_match(state)


class StringMatcher(Matcher):
    def try_match(self, state: LexerState) -> LexerResult | Error:
        state.saveState()
        result = StringMatcher.fetch_string(state)
        if result is Error:
            state.restoreState()
            return super().try_match(state)
        return result

    def fetch_string(state: LexerState) -> LexerResult | Error:
        string = ""
        character = state.next_character()
        while character != None and character != '"':
            if character == "\\" and state.next_character() == '"':
                string += '"'
            elif character == "\\" and state.next_charcter() == "\\":
                string += "\\"
            else:
                string += character
        if string[-1] != '"':
            return Error(
                "Unterminated string literal", "Missing end double quote", state
            )
        return LexerResult(string, state)


class CommentMatcher(Matcher):
    def try_match(self, state: LexerState) -> LexerResult | Error:
        return super().try_match(state)


class NumberMatcher(Matcher):
    def try_match(self, state: LexerState) -> LexerResult | Error:
        return super().try_match(state)


class WordMatcher(Matcher):
    def try_match(self, state: LexerState) -> LexerResult | Error:
        return super().try_match(state)


class Lexer:
    def __init__(self, filepath: str, text: str) -> None:
        self._matcher = OperationMatcher()
        current_matcher = self._matcher
        current_matcher = current_matcher.set_next(StringMatcher())
        current_matcher = current_matcher.set_next(CommentMatcher())
        current_matcher = current_matcher.set_next(NumberMatcher())
        current_matcher = current_matcher.set_next(WordMatcher())
        self._state = LexerState(filepath, text)

    def next(self) -> LexerResult | Error:
        return self._matcher.try_match(self._state)
