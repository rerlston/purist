"""
Purist source code lexer, reads source code and discovers words, numbers, operators, etc
"""

from abc import ABC, abstractmethod
from typing import Self

from purist.utils.errors import DecodeError, Error, InvalidSyntaxError
from purist.utils.logger import Logger
from purist.models.lexer_models import LexerResult, LexerState, LexerType

VALID_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890"
VALID_URL_CHARACTERS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-./_@:[]"
)


class Matcher(ABC):
    def __init__(self):
        self._next_matcher = None

    def set_next(self, matcher):
        self._next_matcher = matcher
        return matcher

    @abstractmethod
    def try_match(self, state: LexerState) -> LexerResult | Error:
        Logger.info(self)
        if self._next_matcher:
            Logger.info(self._next_matcher)
            return self._next_matcher.try_match(state)
        return InvalidSyntaxError("Unrecognised character", state)


class OperatorMatcher(ABC):
    def __init__(self):
        self._next_matcher = None

    def set_next(self, matcher):
        self._next_matcher = matcher
        return matcher

    def get_next(self) -> Self | None:
        return self._next_matcher


class OperationCalculationMatcher(OperatorMatcher):
    def try_match(self, state: LexerState) -> LexerResult | None:
        state.saveState()
        result = self.__fetch_calculation(state)
        if result is None:
            state.restoreState()
        return result

    @classmethod
    def __fetch_calculation(cls, state: LexerState) -> LexerResult | None:
        character, new_line = state.next_character()
        next_character, new_line = state.next_character()
        if character == "=" and next_character == "=":
            return LexerResult(LexerType.CALCULATION_LOGIC, "==", state)

        state.restoreState()
        character, new_line = state.next_character()
        next_character, new_line = state.next_character()
        if character == "!" and next_character == "=":
            return LexerResult(LexerType.CALCULATION_LOGIC, "!=", state)

        state.restoreState()
        character, new_line = state.next_character()
        if character in ["+", "-", "*", "/", "%", "!"]:
            return LexerResult(LexerType.CALCULATION_LOGIC, character, state)
        return None


class OperationGrammarMatcher(OperatorMatcher):
    def try_match(self, state: LexerState) -> LexerResult | None:
        state.saveState()
        result = self.__fetch_grammar(state)
        if result is None:
            state.restoreState()
        return result

    @classmethod
    def __fetch_grammar(cls, state: LexerState) -> LexerResult | None:
        character, new_line = state.next_character()
        if character in ["(", ")", "[", "]", "{", "}"]:
            return LexerResult(LexerType.GRAMMAR_STRUCTURE, character, state)
        return None


class OperationMetaLanguageMatcher(OperatorMatcher):
    def try_match(self, state: LexerState) -> LexerResult | None:
        state.saveState()
        result = self.__fetch_meta_language(state)
        if result is None:
            state.restoreState()
        return result

    @classmethod
    def __fetch_meta_language(cls, state: LexerState) -> LexerResult | None:
        character, new_line = state.next_character()
        Logger.info(character)
        if character in [":", "=", "."]:
            return LexerResult(LexerType.META_LANGUAGE, character, state)
        return None


class SemanticMatcher(Matcher):
    def __init__(self):
        super().__init__()
        self._matcher = OperationCalculationMatcher()
        current_matcher = self._matcher
        current_matcher = current_matcher.set_next(OperationGrammarMatcher())
        current_matcher = current_matcher.set_next(OperationMetaLanguageMatcher())

    def try_match(self, state: LexerState) -> LexerResult | Error:
        state.saveState()
        result = result = self._matcher.try_match(state)
        matcher = self._matcher
        while result is None and matcher is not None:
            result = matcher.try_match(state)
            matcher = matcher.get_next()
        if result is None:
            return super().try_match(state)
        return result


class StringMatcher(Matcher):
    def try_match(self, state: LexerState) -> LexerResult | Error:
        state.saveState()
        result = self.__fetch_string(state)
        if result is None:
            state.restoreState()
            return super().try_match(state)
        return result

    @classmethod
    def __fetch_string(cls, state: LexerState) -> LexerResult | None:
        string = ""
        character, new_line = state.next_character()
        next_character, new_line = state.next_character()
        while character is not None and character != '"' and next_character != '"':
            if character == "\\" and next_character == '"':
                string += '"'
            elif character == "\\" and next_character == "\\":
                string += "\\"
            else:
                string += character + next_character
            character, new_line = state.next_character()
            next_character, new_line = state.next_character()
        if string[-1] != '"':
            return None
        return LexerResult(LexerType.STRING, string, state)


class CommentMatcher(Matcher):
    def try_match(self, state: LexerState) -> LexerResult | Error:
        state.saveState()
        result = self.__fetch_comment(state)
        if result == None:
            state.restoreState()
            return super().try_match(state)

    @classmethod
    def __fetch_comment(cls, state: LexerState) -> LexerResult | None:
        comment = ""
        character, new_line = state.next_character()
        if character == "/" and state.next_character() == "/":
            (character, new_line) = state.next_character()
            Logger.info("detected comment, fetching rest of comment line")
            while new_line:
                comment = comment + character
                (character, new_line) = state.next_character()
                Logger.info(character)
            Logger.info("end of line")
            Logger.info(comment)
        if len(comment) == 0:
            return None
        return LexerResult(LexerType.COMMENT, comment, state)


class NumberMatcher(Matcher):
    def try_match(self, state: LexerState) -> LexerResult | Error:
        return super().try_match(state)


class WordMatcher(Matcher):
    def try_match(self, state: LexerState) -> LexerResult | Error:
        return super().try_match(state)


class Lexer:
    def __init__(self, filepath: str, text: str) -> None:
        self._matcher = SemanticMatcher()
        current_matcher = self._matcher
        current_matcher = current_matcher.set_next(StringMatcher())
        current_matcher = current_matcher.set_next(CommentMatcher())
        current_matcher = current_matcher.set_next(NumberMatcher())
        current_matcher = current_matcher.set_next(WordMatcher())
        self._state = LexerState(filepath, text)

    def next(self) -> LexerResult | Error:
        return self._matcher.try_match(self._state)
