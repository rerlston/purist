import re

from abc import ABC, abstractmethod

from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.errors import Error
from purist.utils.logger import Logger

PASCAL_CASE_CHARACTERS = r"^[A-Z][a-zA-Z0-9]"
CAMEL_CASE_CHARACTERS = r"^[a-z][A-Za-z0-9]"
CONSTANT_CHARACTERS = r"^[A-Z_0-9]+$"

SERVICE_SYNONYMS = r"^(class|service)"
INTENT_SYNONYMS = r"^(interface|intent|contract|portal)"
MODEL_SYNONYMS = r"^(type|model)"
FULFILLS_SYNONYMS = r"^(implements|supports,fulfills|achieves)"
BEHAVES_LIKE_SYNONYMS = r"^(extends|behavesLike|becomes|adopts)"
BLUEPRINT_SYNONYMS = r"^(abstract|blueprint|concept|conceptual|theory|theoretical)"
ENUMERATION_SYNONYMS = r"^(enum|enumeration|values|presets|options|choices)"
BOOLEANS = r"^(true|false)"


class BaseIdentifierMatcher(ABC):
    def __init__(self) -> None:
        self._reserved_words = [
            "private",
            "hidden",
            "public",
            "visible",
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
            "null",
            "or",
            "and",
            "not",
            "equal",
            "greater",
            "less",
            "le",
            "ge",
            "xor",
            "is",
            "in",
            "self",
            "this",
            "virtual",
            "import",
            "from",
            "require",
            "void",
            "print",
        ]

    @abstractmethod
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        pass


class ReservedKeywordMatcher(BaseIdentifierMatcher):
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        Logger.trace("reserved keyword matcher")
        if value in self._reserved_words:
            Logger.trace(f"found: {value}")
            return LexerResult(LexerType.RESERVED_WORD, value, state)

        result = re.match(SERVICE_SYNONYMS, value)
        Logger.trace(f"service match? {result}")
        if bool(result):
            return LexerResult(LexerType.SERVICE, value, state)

        result = re.match(INTENT_SYNONYMS, value)
        Logger.trace(f"intent match? {result}")
        if bool(result):
            return LexerResult(LexerType.INTENT, value, state)

        result = re.match(MODEL_SYNONYMS, value)
        Logger.trace(f"model match? {result}")
        if bool(result):
            return LexerResult(LexerType.MODEL, value, state)

        result = re.match(FULFILLS_SYNONYMS, value)
        Logger.trace(f"fulfills match? {result}")
        if bool(result):
            return LexerResult(LexerType.FULFILLS, value, state)

        result = re.match(BEHAVES_LIKE_SYNONYMS, value)
        Logger.trace(f"behaves like match? {result}")
        if bool(result):
            return LexerResult(LexerType.BEHAVES_LIKE, value, state)

        result = re.match(BLUEPRINT_SYNONYMS, value)
        Logger.trace(f"blueprint match? {result}")
        if bool(result):
            return LexerResult(LexerType.BLUEPRINT, value, state)

        result = re.match(ENUMERATION_SYNONYMS, value)
        Logger.trace(f"enum match? {result}")
        if bool(result):
            return LexerResult(LexerType.ENUMERATION, value, state)

        result = re.match(BOOLEANS, value)
        Logger.trace(f"bool match? {result}")
        if bool(result):
            return LexerResult(LexerType.BOOLEAN_VALUE, value, state)

        return None


class ConstantKeywordMatcher(BaseIdentifierMatcher):
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        Logger.trace("constant keyword matcher")
        result = re.match(CONSTANT_CHARACTERS, value)
        if bool(result):
            Logger.trace(f"found: {value}")
            return LexerResult(LexerType.CONSTANT, value, state)
        return None


class IdentifierKeywordMatcher(BaseIdentifierMatcher):
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        Logger.trace("reserved keyword matcher")
        result = re.match(CAMEL_CASE_CHARACTERS, value)
        if bool(result):
            Logger.trace(f"found: {value}")
            return LexerResult(LexerType.IDENTIFIER, value, state)

        result = re.match(PASCAL_CASE_CHARACTERS, value)
        if bool(result):
            Logger.trace(f"found: {value}")
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
        Logger.trace("word matcher")
        word = ""
        character, new_line = state.next_character()
        if character.isalpha():
            while character is not None and character.isalnum() and not new_line:
                word += character
                character, new_line = state.next_character()
        if len(word) == 0:
            Logger.trace("not found")
            return None
        for matcher in self._matchers:
            result = matcher.try_match(word, state)
            if result is not None:
                return result
        Logger.info("word matcher: not found")
        return LexerResult(LexerType.UNKNOWN, word, state)
