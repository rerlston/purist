import re

from abc import ABC, abstractmethod

from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.errors import Error
from purist.utils.logger import Logger

PASCAL_CASE_CHARACTERS = r"^[A-Z][a-zA-Z0-9]"
CAMEL_CASE_CHARACTERS = r"^[a-z][A-Za-z0-9]"
CONSTANT_CHARACTERS = r"^[A-Z_0-9]+$"


class BaseIdentifierMatcher(ABC):
    def __init__(self) -> None:
        self._reserved_words = [
            "type",
            "service",
            "class",
            "model",
            "interface",
            "contract",
            "portal",
            "enumeration",
            "enum",
            "private",
            "public",
            "constructor",
            "destructor",
            "if",
            "while",
            "new",
            "int",
            "integer",
            "decimal",
            "number",
            "string",
            "bool",
            "boolean",
            "true",
            "false",
            "null",
            "or",
            "and",
            "not",
            "equal",
            "greater",
            "less",
            "is",
            "in",
            "self",
            "this",
            "abstract",
            "concept",
            "conceptual",
            "theory",
            "theoretical",
            "virtual",
            "import",
            "from",
            "require",
            "implements",
            "extends",
            "void",
            "print",
        ]

    @abstractmethod
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        pass


class ReservedKeywordMatcher(BaseIdentifierMatcher):
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        Logger.info("reserved keyword matcher")
        if value in self._reserved_words:
            Logger.info(f"found: {value}")
            return LexerResult(LexerType.RESERVED_WORD, value, state)
        return None


class ConstantKeywordMatcher(BaseIdentifierMatcher):
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        Logger.info("constant keyword matcher")
        result = re.match(CONSTANT_CHARACTERS, value)
        if bool(result):
            Logger.info(f"found: {value}")
            return LexerResult(LexerType.CONSTANT, value, state)
        return None


class IdentifierKeywordMatcher(BaseIdentifierMatcher):
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        Logger.info("reserved keyword matcher")
        result = re.match(CAMEL_CASE_CHARACTERS, value)
        if bool(result):
            Logger.info(f"found: {value}")
            return LexerResult(LexerType.IDENTIFIER, value, state)

        result = re.match(PASCAL_CASE_CHARACTERS, value)
        if bool(result):
            Logger.info(f"found: {value}")
            return LexerResult(LexerType.PASCAL_CASE, value, state)
        return None


class WordMatcher(BaseMatcher):
    def __init__(self) -> None:
        self._matchers: BaseIdentifierMatcher = []
        self._matchers.append(ReservedKeywordMatcher())
        self._matchers.append(ConstantKeywordMatcher())
        self._matchers.append(IdentifierKeywordMatcher())

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | Error:
        Logger.info("word matcher")
        word = ""
        character, new_line = state.next_character()
        if character.isalpha():
            while character is not None and character.isalnum() and not new_line:
                word += character
                character, new_line = state.next_character()
        if len(word) == 0:
            Logger.info("not found")
            return None
        for matcher in self._matchers:
            result = matcher.try_match(word, state)
            if result is not None:
                return result
        Logger.info("not found")
        return LexerResult(LexerType.UNKNOWN, word, state)
