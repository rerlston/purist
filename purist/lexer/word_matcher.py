import re

from abc import ABC, abstractmethod

from typing import Dict, List

from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.logger import Logger

PASCAL_CASE_CHARACTERS = r"^[A-Z][a-zA-Z0-9]*$"
CAMEL_CASE_CHARACTERS = r"^[a-zA-Z][A-Za-z0-9]*$"
CONSTANT_CHARACTERS = r"^[A-Z_0-9]{2,}+$"
# CONSTANT_CHARACTERS = r"^(?:[A-Z]+_[0-9]+|[0-9]+_[A-Z]+)(?:_[A-Z0-9]+)*$"
# CONSTANT_CHARACTERS = r"\b[A-Z][A-Z0-9_]*[A-Z0-9]\b|\b[A-Z]\b"

SERVICE_SYNONYMS = r"^(class|service)"
INTENT_SYNONYMS = r"^(interface|intent|contract|portal)"
MODEL_SYNONYMS = r"^(type|model)"
FULFILLS_SYNONYMS = r"^(implements|supports,fulfills|achieves)"
BEHAVES_LIKE_SYNONYMS = r"^(extends|behavesLike|becomes|adopts|prototype)"
BLUEPRINT_SYNONYMS = (
    r"^(abstract|blueprint|concept|conceptual|theory|theoretical|protocol)"
)
ENUMERATION_SYNONYMS = r"^(enum|enumeration|values|presets|options|choices)"
BOOLEANS = r"^(true|false)"


class BaseIdentifierMatcher(ABC):
    def __init__(self) -> None:
        self._reserved_words: Dict[str, LexerType] = {
            "private": LexerType.PRIVATE,
            "hidden": LexerType.PRIVATE,
            "public": LexerType.PUBLIC,
            "visible": LexerType.PUBLIC,
            "constructor": LexerType.CONSTRUCTOR,
            "destructor": LexerType.DESTRUCTOR,
            "if": LexerType.IF,
            "while": LexerType.WHILE,
            "new": LexerType.NEW,
            "int": LexerType.NUMBER_TYPE,
            "integer": LexerType.NUMBER_TYPE,
            "decimal": LexerType.FLOAT_TYPE,
            "number": LexerType.FLOAT_TYPE,
            "string": LexerType.STRING_TYPE,
            "bool": LexerType.BOOL_TYPE,
            "boolean": LexerType.BOOL_TYPE,
            "null": LexerType.NULL,
            "or": LexerType.LOGICAL_OR,
            "and": LexerType.LOGICAL_AND,
            "not": LexerType.LOGICAL_NOT,
            "equal": LexerType.EQUALS,
            "greater": LexerType.GREATER_THAN,
            "greaterOrEqual": LexerType.GREATER_OR_EQUAL,
            "less": LexerType.LESS_THAN,
            "lessOrEqual": LexerType.LESS_OR_EQUAL,
            "le": LexerType.LESS_OR_EQUAL,
            "ge": LexerType.GREATER_OR_EQUAL,
            "xor": LexerType.XOR,
            "is": LexerType.IS,
            "in": LexerType.IN,
            "self": LexerType.THIS,
            "this": LexerType.THIS,
            "virtual": LexerType.VIRTUAL,
            "import": LexerType.IMPORT,
            "from": LexerType.FROM,
            "require": LexerType.REQUIRE,
            "void": LexerType.VOID,
            "true": LexerType.TRUE,
            "false": LexerType.FALSE,
            "date": LexerType.DATE_TYPE,
            "ne": LexerType.NOT_EQUALS,
            "eq": LexerType.EQUALS,
            "return": LexerType.RETURN,
            "super": LexerType.SUPER,
        }

    @abstractmethod
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        pass


class ReservedKeywordMatcher(BaseIdentifierMatcher):
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        Logger.trace("reserved keyword matcher")
        if value in self._reserved_words:
            Logger.trace(f"found: {value}")
            return LexerResult(self._reserved_words[value], value, state)

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
            return LexerResult(LexerType.DEFINITION, value, state)
        return None


class WordMatcher(BaseMatcher):

    def __init__(self, matchers: List[BaseIdentifierMatcher]) -> None:
        self._matchers = matchers

    @classmethod
    def setup(self) -> List[BaseIdentifierMatcher]:
        matchers: list[BaseIdentifierMatcher] = []
        matchers.append(ReservedKeywordMatcher())
        matchers.append(ConstantKeywordMatcher())
        matchers.append(IdentifierKeywordMatcher())
        return matchers

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        Logger.trace("word matcher")
        word = ""
        Logger.trace(state)
        character, new_line = state.next_character()
        if character is not None and character.isalpha():
            while (
                character is not None
                and (character.isalnum() or character == "_")
                and not new_line
            ):
                word += character
                character, new_line = state.peek_next_character()
                if character is not None and (character.isalnum() or character == "_"):
                    character, new_line = state.next_character()
            if new_line and character is not None and character.isalnum():
                word += character
        Logger.trace(state)
        if len(word) == 0:
            Logger.trace("not found")
            return None
        for matcher in self._matchers:
            result = matcher.try_match(word, state)
            if result is not None:
                Logger.trace(result.type)
                return result
        Logger.trace("word matcher: not found")
        return LexerResult(LexerType.UNKNOWN, word, state)
