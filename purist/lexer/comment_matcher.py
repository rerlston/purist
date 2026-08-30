from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.logger import Logger


class CommentMatcher(BaseMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        Logger.trace("comment matcher")
        comment = ""
        character, new_line = state.next_character()
        next_character, new_line = state.peek_next_character()
        if character == "/" and next_character == "/":
            next_character, new_line = state.next_character()
            comment = "//"
            Logger.trace("comment characters found")
            character, new_line = state.next_character()
            while not new_line:
                Logger.trace(character)
                comment = comment + character
                character, new_line = state.peek_next_character()
                if not new_line:
                    character, new_line = state.next_character()
            Logger.trace(comment)
        if len(comment) == 0:
            Logger.trace("not found")
            return None
        Logger.trace(f"found: {comment}")
        return LexerResult(LexerType.COMMENT, comment, state)
