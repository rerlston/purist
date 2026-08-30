from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.logger import Logger


class NumberMatcher(BaseMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        Logger.trace("number matcher")
        string = ""
        character, new_line = state.next_character()
        Logger.trace(character)
        if character is not None and (character == "-" or character.isdigit()):
            string += character
            character, new_line = state.next_character()
            while not new_line and character.isdigit() or character == ".":
                string += character
                character, new_line = state.peek_next_character()
                if not new_line and character.isdigit() or character == ".":
                    character, new_line = state.next_character()
            if character.isdigit() or character == ".":
                string += character
        Logger.trace("(" + string + ")")
        if len(string) > 0:
            try:
                float(string)
                Logger.trace(f"found: {string}")
                if "." in string:
                    return LexerResult(LexerType.FLOAT_LITERAL, string, state)
                return LexerResult(LexerType.NUMBER_LITERAL, string, state)
            except ValueError:
                pass

        Logger.trace("not found")
        return None
