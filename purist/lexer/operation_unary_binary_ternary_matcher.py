from abc import ABC, abstractmethod
from typing import List

from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, TokenType
from purist.utils.logger import Logger


class BaseOperatorMatcher(ABC):
    @abstractmethod
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        pass


# unary: logical not (!), increment (++), decrement (--), negation (-, e.g. (-(-5) = 5))
class OperationUnaryNotOperatorMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None:
            character, new_line = state.next_character()
            previous_type = previous_match.type
            Logger.trace(f"previous: {previous_type}")
            if previous_type == TokenType.ASSIGN:
                if character == "!":
                    Logger.trace("found: !")
                    return LexerResult(TokenType.LOGICAL_NOT, character, state)
        return None


class OperationUnaryIncrementOperatorMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None:
            character1, new_line = state.next_character()
            character2, new_line = state.peek_next_character()
            Logger.trace(f"previous: {previous_match.type}")
            if previous_match.type == TokenType.IDENTIFIER:
                if character1 == "+" and character2 == "+":
                    character2, new_line = state.next_character()
                    Logger.trace("found: ++")
                    return LexerResult(TokenType.INCREMENT, "++", state)
        return None


class OperationUnaryDecrementOperatorMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None:
            character1, new_line = state.next_character()
            character2, new_line = state.peek_next_character()
            Logger.trace(f"previous: {previous_match.type}")
            if previous_match.type == TokenType.IDENTIFIER:
                if character1 == "-" and character2 == "-":
                    Logger.trace("found: --")
                    character2, new_line = state.next_character()
                    return LexerResult(TokenType.DECREMENT, "--", state)
        return None


class OperationUnaryNegationOperatorMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None:
            character, new_line = state.next_character()
            Logger.trace(f"previous: {previous_match.type}")
            if previous_match.type in [TokenType.ASSIGN, TokenType.L_ROUND]:
                if character == "-":
                    Logger.trace("found: -")
                    return LexerResult(TokenType.NEGATION, character, state)
        return None


# binary: addition (+), subtraction (-), multiplication (*), mod (%), divide (/), assignment (=), comparison (==, <, >, !=, <=, >=), logical or (||), logical and (&&), binary or (|), binary and (&), binary xor (^), power (**)
class OperationBinaryMathsOperatorMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None:
            character1, new_line = state.next_character()
            character2, new_line = state.peek_next_character()
            Logger.trace(f"previous: {previous_match.type}")
            if previous_match.type in [
                TokenType.NUMBER_LITERAL,
                TokenType.IDENTIFIER,
            ]:
                if character1 == "+":
                    Logger.trace(f"found: {character1}")
                    return LexerResult(TokenType.ADDITION, character1, state)
                if character1 == "-":
                    Logger.trace(f"found: {character1}")
                    return LexerResult(TokenType.SUBTRACTION, character1, state)
                if character1 == "%":
                    Logger.trace(f"found: {character1}")
                    return LexerResult(TokenType.MOD, character1, state)
                if character1 == "^":
                    Logger.trace(f"found: {character1}")
                    return LexerResult(TokenType.XOR, character1, state)
                if character1 == "/":
                    if character2 == "/":
                        return None
                    else:
                        Logger.trace("found: /")
                        return LexerResult(TokenType.DIVIDE, character1, state)
                if character1 == "*":
                    if character2 == "*":
                        character2, new_line = state.next_character()
                        Logger.trace("found: **")
                        return LexerResult(TokenType.POWER, "**", state)
                    else:
                        Logger.trace("found: *")
                        return LexerResult(TokenType.MULTIPLY, character1, state)
            return None


class OperationBinaryAssignmentMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None:
            Logger.debug(f"previous: {previous_match.type}")
            if previous_match.type in [TokenType.IDENTIFIER, TokenType.CONSTANT]:
                character1, new_line = state.next_character()
                character2, new_line = state.peek_next_character()
                Logger.debug(f"{character1}<{character2}>")
                if character1 == "=":
                    if character2 == "=":
                        character2, new_line = state.next_character()
                        Logger.trace("found: ==")
                        return LexerResult(TokenType.EQUALS, "==", state)
                    else:
                        Logger.trace("found: =")
                        return LexerResult(TokenType.ASSIGN, character1, state)
            return None


class OperationBinaryNegativeComparisonMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None and previous_match.type in [
            TokenType.NUMBER_LITERAL,
            TokenType.IDENTIFIER,
        ]:
            character1, new_line = state.next_character()
            character2, new_line = state.peek_next_character()
            if character1 == "!" and character2 == "=":
                Logger.trace("found: !=")
                character2, new_line = state.next_character()
                return LexerResult(TokenType.NOT_EQUALS, "!=", state)
        return None


class OperationBinaryGreaterComparisonMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None and previous_match.type in [
            TokenType.NUMBER_LITERAL,
            TokenType.IDENTIFIER,
        ]:
            character1, new_line = state.next_character()
            character2, new_line = state.peek_next_character()
            if character1 == ">":
                if character2 == "=":
                    character2, new_line = state.next_character()
                    Logger.trace("found: >=")
                    return LexerResult(TokenType.GREATER_OR_EQUAL, ">=", state)
                else:
                    Logger.trace("found: >")
                    return LexerResult(TokenType.GREATER_THAN, ">", state)
        return None


class OperationBinaryLessorComparisonMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None and previous_match.type in [
            TokenType.NUMBER_LITERAL,
            TokenType.IDENTIFIER,
        ]:
            character1, new_line = state.next_character()
            character2, new_line = state.peek_next_character()
            if character1 == "<":
                if character2 == "=":
                    character2, new_line = state.next_character()
                    Logger.trace("found: <=")
                    return LexerResult(TokenType.LESS_OR_EQUAL, "<=", state)
                else:
                    Logger.trace("found: <")
                    return LexerResult(TokenType.LESS_THAN, "<", state)
            return None


class OperationBinaryOrMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None and previous_match.type in [
            TokenType.NUMBER_LITERAL,
            TokenType.IDENTIFIER,
        ]:
            character1, new_line = state.next_character()
            character2, new_line = state.peek_next_character()
            if character1 == "|":
                if character2 == "|":
                    character2, new_line = state.next_character()
                    Logger.trace("found: ||")
                    return LexerResult(TokenType.LOGICAL_OR, "||", state)
                else:
                    Logger.trace("found: |")
                    return LexerResult(TokenType.MATH_OR, "|", state)
            return None


class OperationBinaryAndMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None and previous_match.type in [
            TokenType.NUMBER_LITERAL,
            TokenType.IDENTIFIER,
        ]:
            character1, nwe_line = state.next_character()
            character2, new_line = state.peek_next_character()
            if character1 == "&":
                if character2 == "&":
                    character2, new_line = state.next_character()
                    Logger.trace("found: &&")
                    return LexerResult(TokenType.LOGICAL_AND, "&&", state)
                else:
                    Logger.trace("found: &")
                    return LexerResult(TokenType.MATH_AND, "&", state)
            return None


class OperationBinaryStringConcatenationMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None:
            if previous_match.type == TokenType.STRING_LITERAL:
                character, new_line = state.next_character()
                if character == "+":
                    Logger.trace(f"found: {character}")
                    return LexerResult(TokenType.STRING_CONCATENATION, character, state)
        return None


# ternary: if-else (? :)
class OperationTernaryMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        if previous_match is not None:
            if previous_match.type in [
                TokenType.NUMBER_LITERAL,
                TokenType.STRING_LITERAL,
                TokenType.TRUE,
                TokenType.FALSE,
                TokenType.IDENTIFIER,
                TokenType.R_ROUND,
            ]:
                character, new_line = state.next_character()
                if character == "?":
                    Logger.trace(f"found: {character}")
                    return LexerResult(TokenType.QUESTION, character, state)
                if character == ":":
                    Logger.trace(f"found: {character}")
                    return LexerResult(TokenType.COLON, character, state)
        return None


class OperationCalculationMatcher(BaseMatcher):

    def __init__(self, matchers: List[BaseOperatorMatcher]) -> None:
        self._matchers = matchers

    @classmethod
    def setup(cls) -> List[BaseOperatorMatcher]:
        response: List[BaseOperatorMatcher] = []
        response.append(OperationUnaryNotOperatorMatcher())
        response.append(OperationUnaryIncrementOperatorMatcher())
        response.append(OperationUnaryDecrementOperatorMatcher())
        response.append(OperationUnaryNegationOperatorMatcher())

        response.append(OperationBinaryMathsOperatorMatcher())
        response.append(OperationBinaryAssignmentMatcher())
        response.append(OperationBinaryNegativeComparisonMatcher())
        response.append(OperationBinaryGreaterComparisonMatcher())
        response.append(OperationBinaryLessorComparisonMatcher())
        response.append(OperationBinaryOrMatcher())
        response.append(OperationBinaryAndMatcher())
        response.append(OperationBinaryStringConcatenationMatcher())

        response.append(OperationTernaryMatcher())

        return response

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        Logger.trace("calulation matcher")
        for matcher in self._matchers:
            state_copy = state.clone()
            result = matcher.try_match(state_copy, previous_match)
            if result is not None:
                return result
            # state.restore()
        Logger.trace("calculation matcher: not found")
        return None
