from typing import Dict

from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.logger import Logger


class OperationBracketMatcher(BaseMatcher):

    def __init__(self) -> None:
        self.BRACKETS: Dict[str, LexerType] = {
            "(": LexerType.L_ROUND,
            ")": LexerType.R_ROUND,
            "[": LexerType.L_SQUARE,
            "]": LexerType.R_SQUARE,
            "{": LexerType.L_CURLY,
            "}": LexerType.R_CURLY,
            "<": LexerType.L_ANGLE,
            ">": LexerType.R_ANGLE,
        }

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        Logger.trace("bracket matcher")
        character, new_line = state.next_character()
        if not new_line:
            if character in self.BRACKETS.keys():
                Logger.trace(f"found: {character}")
                return LexerResult(self.BRACKETS[character], character, state)
        Logger.trace("not found")
        return None
