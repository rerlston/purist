from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.errors import Error
from purist.utils.logger import Logger


class OperationMetaLanguageMatcher(BaseMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | Error:
        Logger.info("meta language matcher")
        string = state.peek()
        previous_type = "None"
        if previous_match is not None:
            previous_type = previous_match.type
        Logger.info(f"string: [{string}], previous: {previous_type}")
        if len(string) > 0:
            if previous_match is not None:
                Logger.info(previous_match.type)
                if previous_match.type == LexerType.IDENTIFIER:
                    if string[0] in [":", "=", "."]:
                        Logger.info(f"found: {string[0]}")
                        return LexerResult(LexerType.META_LANGUAGE, string[0], state)
        Logger.info("not found")
        return None
