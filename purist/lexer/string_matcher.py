from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, TokenType
from purist.utils.logger import Logger


class StringMatcher(BaseMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        Logger.trace("string matcher")
        string = ""
        character, new_line = state.next_character()
        next_character, new_line = state.next_character()
        if character is not None and next_character is not None:
            if character == "\\":
                Logger.trace(
                    "double quoted string in python with escaped double quotes value found"
                )
                while (
                    character is not None
                    and character != '"'
                    and next_character is not None
                    and next_character != '"'
                ):
                    if character == "\\" and next_character == '"':
                        string += '"'
                    elif character == "\\" and next_character == "\\":
                        string += "\\"
                    else:
                        string += character + next_character
                    character, new_line = state.next_character()
                    next_character, new_line = state.next_character()
                    if new_line:
                        string += "\n"
            elif character == '"':
                string += character + next_character
                character, new_line = state.next_character()
                while character is not None and character != '"':
                    if new_line:
                        string += "\n"
                    string += character
                    character, new_line = state.next_character()
                string += '"'
        if len(string) > 0 and string[-1] != '"':
            Logger.trace("not found")
            return None
        if len(string) == 0:
            Logger.trace("not found")
            return None
        Logger.trace(f"found: {string}")
        return LexerResult(TokenType.STRING_LITERAL, string, state)
