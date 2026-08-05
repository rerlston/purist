from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.errors import Error
from purist.utils.logger import Logger


class NumberMatcher(BaseMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | Error:
        Logger.info("number matcher")
        string = ""
        character, new_line = state.next_character()
        Logger.info(character)
        if character is not None and (character in ["-", "+"] or character.isdigit()):
            string += character
            character, new_line = state.next_character()
            while not new_line and character.isdigit() or character == ".":
                string += character
                character, new_line = state.next_character()
            if not new_line:
                state.step_back()
        Logger.info("(" + string + ")")
        if len(string) > 0:
            try:
                float(string)
                Logger.info(f"found: {string}")
                if previous_match is None:
                    return LexerResult(LexerType.NUMBER, string, state)
            except ValueError:
                pass

        Logger.info("not found")
        return None
