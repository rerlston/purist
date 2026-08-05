from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.errors import Error
from purist.utils.logger import Logger


class CommentMatcher(BaseMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | Error:
        Logger.info("comment matcher")
        comment = ""
        character, new_line = state.next_character()
        next_character, new_line = state.next_character()
        if character == "/" and next_character == "/":
            comment = "//"
            Logger.info("comment characters found")
            character, new_line = state.next_character()
            while not new_line:
                Logger.info(character)
                comment = comment + character
                character, new_line = state.next_character()
            Logger.info(comment)
        if len(comment) == 0:
            Logger.info("not found")
            return None
        Logger.info(f"found: {comment}")
        return LexerResult(LexerType.COMMENT, comment, state)
