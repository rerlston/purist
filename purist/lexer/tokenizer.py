"""
Purist source code lexer, reads source code and discovers words, numbers, operators, etc
"""

from typing import List
from purist.lexer.base_matcher import BaseMatcher
from purist.lexer.comment_matcher import CommentMatcher
from purist.lexer.number_matcher import NumberMatcher
from purist.lexer.operation_unary_binary_ternary_matcher import (
    OperationCalculationMatcher,
)
from purist.lexer.operation_bracket_matcher import OperationBracketMatcher
from purist.lexer.operation_meta_language_matcher import OperationMetaLanguageMatcher
from purist.lexer.string_matcher import StringMatcher
from purist.lexer.word_matcher import WordMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.errors import Error, InvalidSyntaxError
from purist.utils.logger import Logger


class LargestConsumer:
    def __init__(self):
        self._matcher = None
        self._length = 0
        self._lexer_result = None
        self._state = None

    @property
    def matcher(self) -> BaseMatcher | None:
        return self._matcher

    @matcher.setter
    def matcher(self, new_matcher: BaseMatcher | None) -> None:
        self._matcher = new_matcher

    @property
    def length(self) -> int:
        return self._length

    @length.setter
    def length(self, new_length: int) -> None:
        self._length = new_length

    @property
    def lexer_result(self) -> LexerResult | None:
        return self._lexer_result

    @lexer_result.setter
    def lexer_result(self, new_lexer_result: LexerResult) -> None:
        self._lexer_result = new_lexer_result

    @property
    def state(self) -> LexerState | None:
        return self._state

    @state.setter
    def state(self, new_state: LexerState) -> None:
        self._state = new_state


class Tokenizer:

    def __init__(self, matchers: List[BaseMatcher], start_state: LexerState):
        self._matchers = matchers
        self._state = start_state
        self._previous_result = None

    @classmethod
    def setup(cls) -> List[BaseMatcher]:
        response: List[BaseMatcher] = []
        calculation_matchers = OperationCalculationMatcher.setup()
        response.append(OperationCalculationMatcher(calculation_matchers))
        response.append(OperationBracketMatcher())
        response.append(OperationMetaLanguageMatcher())
        response.append(StringMatcher())
        response.append(CommentMatcher())
        response.append(NumberMatcher())
        word_matchers = WordMatcher.setup()
        response.append(WordMatcher(word_matchers))

        return response

    def next(self) -> LexerResult | Error:
        Logger.debug("--------------------------------------------")
        largest = LargestConsumer()
        Logger.trace(f"pre skip: {self._state}")

        self._state.skip_spaces()

        Logger.trace(f"post skip: {self._state}")

        if not self._state.is_eof():
            for matcher in self._matchers:
                state = self._state.clone()
                # Logger.info(f"{state}")
                result = matcher.try_match(state, self._previous_result)
                if result is not None:
                    Logger.debug(result)
                    self._store_if_largest(matcher, result, largest)
                # state.restore()
                # state.skip_spaces()

            response = largest.lexer_result
            self._previous_result = response

            if response is not None:
                self._state = largest.state
                self._state.consume()
                return response

        if self._state.is_eof():
            return LexerResult(LexerType.EOF, "", self._state)

        return InvalidSyntaxError(self._state.peek_next_character(), self._state)

    def _store_if_largest(
        self,
        matcher: BaseMatcher | None,
        result: LexerResult | None,
        largest: LargestConsumer,
    ) -> None:
        if result is not None and result.type is not None and result.value is not None:
            consumed_length = len(result.value)
            if largest.matcher is None or consumed_length > largest.length:
                Logger.trace(f"new largest matcher: {result.type}")
                largest.matcher = matcher
                largest.length = consumed_length
                largest.state = result.state.clone()
                largest.lexer_result = result
