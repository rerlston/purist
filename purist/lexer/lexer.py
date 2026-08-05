"""
Purist source code lexer, reads source code and discovers words, numbers, operators, etc
"""

from purist.lexer.base_matcher import BaseMatcher
from purist.lexer.comment_matcher import CommentMatcher
from purist.lexer.number_matcher import NumberMatcher
from purist.lexer.operation_unary_binary_ternary_matcher import (
    OperationCalculationMatcher,
)
from purist.lexer.operation_grammer_matcher import OperationGrammarMatcher
from purist.lexer.operation_meta_language_matcher import OperationMetaLanguageMatcher
from purist.lexer.string_matcher import StringMatcher
from purist.lexer.word_matcher import WordMatcher
from purist.models.lexer_models import LexerResult, LexerState
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
    def matcher(self, new_matcher: BaseMatcher) -> None:
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


class Lexer:
    def __init__(self, filepath: str, text: str) -> None:
        self._matchers = []
        self._matchers.append(OperationCalculationMatcher())
        self._matchers.append(OperationGrammarMatcher())
        self._matchers.append(OperationMetaLanguageMatcher())
        self._matchers.append(StringMatcher())
        self._matchers.append(CommentMatcher())
        self._matchers.append(NumberMatcher())
        self._matchers.append(WordMatcher())
        self._state = LexerState(filepath, text)
        self._previous_result = None

    def next(self) -> LexerResult | Error:
        Logger.info("--------------------------------------------")
        largest = LargestConsumer()
        Logger.info(f"peek: [{self._state.peek()}]")

        self.__trim_peekable(self._state)

        Logger.info(f"[{self._state.peek()}]")

        for matcher in self._matchers:
            state_copy = self.__make_copy(self._state)

            result = matcher.try_match(state_copy, self._previous_result)
            self.__store_if_largest(matcher, result, largest)

        response = self.__fetch_largest(largest, self._state)

        if response is not None:
            return response
        return InvalidSyntaxError(state_copy.peek(), state_copy)

    @classmethod
    def __trim_peekable(self, state: LexerState) -> None:
        current_character, new_line = state.next_character()
        if current_character == " ":
            while current_character == " ":
                current_character, new_line = state.next_character()
            Logger.info(f"peek: [{state.peek()}]")
        state.step_back()

    @classmethod
    def __make_copy(self, state: LexerState):
        return state.clone()

    @classmethod
    def __fetch_largest(
        self, largest: LargestConsumer, state: LexerState
    ) -> LexerResult | None:
        if largest.matcher is not None:
            Logger.info(largest.lexer_result.type)
            state_copy = largest.state
            value = largest.lexer_result.value
            new_index = state.column + len(value)
            Logger.info(f"previous column: {state.column}")
            Logger.info(f"new column: {new_index}")
            Logger.info(f"previous line: {state.line}")
            Logger.info(f"new line: {state_copy.line}")
            new_line = state.set_new_state(new_index, state_copy.line)
            self._previous_result = largest.lexer_result
            Logger.info(largest.lexer_result.value)
            return largest.lexer_result
        return None

    @classmethod
    def __store_if_largest(
        self,
        matcher: BaseMatcher | None,
        result: LexerResult | None,
        largest: LargestConsumer,
    ) -> None:
        if result is not None and result.type is not None:
            consumed_length = len(result.value)
            if largest.matcher is None or consumed_length > largest.length:
                Logger.info(f"new matcher: {result.type}")
                largest.matcher = matcher
                largest.length = consumed_length
                largest.state = matcher.state
                largest.lexer_result = result
