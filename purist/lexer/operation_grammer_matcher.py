from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.errors import Error
from purist.utils.logger import Logger


class OperationGrammarMatcher(BaseMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | Error:
        Logger.info("grammar matcher")
        string = state.peek()
        if len(string) > 0:
            if string[0] in ["(", ")", "[", "]", "{", "}"]:
                Logger.info(f"found: {string[0]}")
                return LexerResult(LexerType.GRAMMAR_STRUCTURE, string[0], state)
        Logger.info("not found")
        return None
