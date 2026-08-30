import re

from abc import ABC, abstractmethod

from typing import Dict, List

from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, TokenType
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
        self._reserved_words: Dict[str, TokenType] = {
            "private": TokenType.PRIVATE,
            "hidden": TokenType.PRIVATE,
            "public": TokenType.PUBLIC,
            "visible": TokenType.PUBLIC,
            "constructor": TokenType.CONSTRUCTOR,
            "destructor": TokenType.DESTRUCTOR,
            "if": TokenType.IF,
            "while": TokenType.WHILE,
            "new": TokenType.NEW,
            "int": TokenType.NUMBER_TYPE,
            "integer": TokenType.NUMBER_TYPE,
            "decimal": TokenType.FLOAT_TYPE,
            "number": TokenType.FLOAT_TYPE,
            "string": TokenType.STRING_TYPE,
            "bool": TokenType.BOOL_TYPE,
            "boolean": TokenType.BOOL_TYPE,
            "null": TokenType.NULL,
            "or": TokenType.LOGICAL_OR,
            "and": TokenType.LOGICAL_AND,
            "not": TokenType.LOGICAL_NOT,
            "equal": TokenType.EQUALS,
            "greater": TokenType.GREATER_THAN,
            "greaterOrEqual": TokenType.GREATER_OR_EQUAL,
            "less": TokenType.LESS_THAN,
            "lessOrEqual": TokenType.LESS_OR_EQUAL,
            "le": TokenType.LESS_OR_EQUAL,
            "ge": TokenType.GREATER_OR_EQUAL,
            "xor": TokenType.XOR,
            "is": TokenType.IS,
            "in": TokenType.IN,
            "self": TokenType.THIS,
            "this": TokenType.THIS,
            "virtual": TokenType.VIRTUAL,
            "import": TokenType.IMPORT,
            "from": TokenType.FROM,
            "require": TokenType.REQUIRE,
            "void": TokenType.VOID,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "date": TokenType.DATE_TYPE,
            "ne": TokenType.NOT_EQUALS,
            "eq": TokenType.EQUALS,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
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
            return LexerResult(TokenType.SERVICE, value, state)

        result = re.match(INTENT_SYNONYMS, value)
        Logger.trace(f"intent match? {result}")
        if bool(result):
            return LexerResult(TokenType.INTENT, value, state)

        result = re.match(MODEL_SYNONYMS, value)
        Logger.trace(f"model match? {result}")
        if bool(result):
            return LexerResult(TokenType.MODEL, value, state)

        result = re.match(FULFILLS_SYNONYMS, value)
        Logger.trace(f"fulfills match? {result}")
        if bool(result):
            return LexerResult(TokenType.FULFILLS, value, state)

        result = re.match(BEHAVES_LIKE_SYNONYMS, value)
        Logger.trace(f"behaves like match? {result}")
        if bool(result):
            return LexerResult(TokenType.BEHAVES_LIKE, value, state)

        result = re.match(BLUEPRINT_SYNONYMS, value)
        Logger.trace(f"blueprint match? {result}")
        if bool(result):
            return LexerResult(TokenType.BLUEPRINT, value, state)

        result = re.match(ENUMERATION_SYNONYMS, value)
        Logger.trace(f"enum match? {result}")
        if bool(result):
            return LexerResult(TokenType.ENUMERATION, value, state)

        return None


class ConstantKeywordMatcher(BaseIdentifierMatcher):
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        Logger.trace("constant keyword matcher")
        result = re.match(CONSTANT_CHARACTERS, value)
        if bool(result):
            Logger.trace(f"found: {value}")
            return LexerResult(TokenType.CONSTANT, value, state)
        return None


class IdentifierKeywordMatcher(BaseIdentifierMatcher):
    def try_match(self, value: str, state: LexerState) -> LexerResult | None:
        Logger.trace("reserved keyword matcher")
        result = re.match(CAMEL_CASE_CHARACTERS, value)
        if bool(result):
            Logger.trace(f"found: {value}")
            return LexerResult(TokenType.IDENTIFIER, value, state)

        result = re.match(PASCAL_CASE_CHARACTERS, value)
        if bool(result):
            Logger.trace(f"found: {value}")
            return LexerResult(TokenType.DEFINITION, value, state)
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
        return LexerResult(TokenType.UNKNOWN, word, state)
