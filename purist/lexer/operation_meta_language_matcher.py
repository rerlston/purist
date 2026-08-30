from typing import Dict

from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, TokenType
from purist.utils.logger import Logger


class OperationMetaLanguageMatcher(BaseMatcher):

    def __init__(self) -> None:
        self.SPECIAL_CHARACTERS: Dict[str, TokenType] = {
            ".": TokenType.PERIOD,
            "@": TokenType.AT,
            "/": TokenType.PATH_SEPARATOR,
            ",": TokenType.COMMA,
            ":": TokenType.COLON,
        }

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        Logger.trace("meta language matcher")
        Logger.trace("bracket matcher")
        character, new_line = state.next_character()
        if not new_line:
            if character in self.SPECIAL_CHARACTERS.keys():
                Logger.trace(f"found: {character}")
                return LexerResult(self.SPECIAL_CHARACTERS[character], character, state)
        Logger.trace("not found")
        return None
