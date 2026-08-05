from abc import ABC, abstractmethod

from purist.lexer.base_matcher import BaseMatcher
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.errors import Error
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
        string = state.peek()
        if previous_match is not None:
            Logger.info(f"previous: {previous_match.type}")
            if previous_match.type == LexerType.BINARY_LOGIC:
                if string[0] == "!":
                    Logger.info("found: !")
                    return LexerResult(LexerType.UNARY_LOGIC, string[0], state)
        return None


class OperationUnaryIncrementOperatorMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None:
            Logger.info(f"previous: {previous_match.type}")
            if previous_match.type == LexerType.IDENTIFIER:
                if string[0] == "+" and string[1] == "+":
                    Logger.info("found: ++")
                    return LexerResult(LexerType.UNARY_LOGIC, string[0], state)
        return None


class OperationUnaryDecrementOperatorMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None:
            Logger.info(f"previous: {previous_match.type}")
            if previous_match.type == LexerType.IDENTIFIER:
                if string[0] == "-" and string[1] == "-":
                    Logger.info("found: --")
                    return LexerResult(LexerType.UNARY_LOGIC, string[0], state)
        return None


class OperationUnaryNegationOperatorMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None:
            Logger.info(f"previous: {previous_match.type}")
            if previous_match.type == LexerType.BINARY_LOGIC:
                if string[0] == "-":
                    Logger.info("found: -")
                    return LexerResult(LexerType.UNARY_LOGIC, string[0], state)
        return None


# binary: addition (+), subtraction (-), multiplication (*), mod (%), divide (/), assignment (=), comparison (==, <, >, !=, <=, >=), logical or (||), logical and (&&), binary or (|), binary and (&), binary xor (^), power (**)
class OperationBinaryOperatorMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None:
            Logger.info(f"previous: {previous_match.type}")
            if previous_match.type in [
                LexerType.NUMBER,
                LexerType.IDENTIFIER,
            ]:
                if string[0] in ["+", "-", "%", "^"]:
                    Logger.info(f"found: {string[0]}")
                    return LexerResult(LexerType.BINARY_LOGIC, string[0], state)
                if string[0] == "/":
                    if string[1] == "/":
                        return None
                    else:
                        Logger.info("found: /")
                        return LexerResult(LexerType.BINARY_LOGIC, string[0], state)
                if string[0] == "*":
                    if string[1] == "*":
                        Logger.info("found: **")
                        return LexerResult(LexerType.BINARY_LOGIC, "**", state)
                    else:
                        Logger.info("found: *")
                        return LexerResult(LexerType.BINARY_LOGIC, string[0], state)
            return None


class OperationBinaryAssignmentMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None:
            Logger.info(f"previous: {previous_match.type}")
            if previous_match.type == LexerType.IDENTIFIER:
                if string[0] == "=":
                    if string[1] == "=":
                        Logger.info("found: ==")
                        return LexerResult(LexerType.BINARY_LOGIC, "==", state)
                    else:
                        Logger.info("found: =")
                        return LexerResult(LexerType.BINARY_LOGIC, string[0], state)
            return None


class OperationBinaryNegativeComparisonMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None and previous_match in [
            LexerType.NUMBER,
            LexerType.IDENTIFIER,
        ]:
            if string[0] == "!" and string[1] == "=":
                Logger.info("found: !=")
                return LexerResult(LexerType.BINARY_LOGIC, "!=", state)
        return None


class OperationBinaryGreaterComparisonMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None and previous_match in [
            LexerType.NUMBER,
            LexerType.IDENTIFIER,
        ]:
            if string[0] == ">":
                if string[1] == "=":
                    Logger.info("found: >=")
                    return LexerResult(LexerType.BINARY_LOGIC, ">=", state)
                else:
                    Logger.info("found: >")
                    return LexerResult(LexerType.BINARY_LOGIC, ">", state)
        return None


class OperationBinaryLessorComparisonMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None and previous_match in [
            LexerType.NUMBER,
            LexerType.IDENTIFIER,
        ]:
            if string[0] == "<":
                if string[1] == "=":
                    Logger.info("found: <=")
                    return LexerResult(LexerType.BINARY_LOGIC, "<=", state)
                else:
                    Logger.info("found: <")
                    return LexerResult(LexerType.BINARY_LOGIC, "<", state)
            return None


class OperationBinaryOrMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None and previous_match in [
            LexerType.NUMBER,
            LexerType.IDENTIFIER,
        ]:
            if string[0] == "|":
                if string[1] == "|":
                    Logger.info("found: ||")
                    return LexerResult(LexerType.BINARY_LOGIC, "||", state)
                else:
                    Logger.info("found: |")
                    return LexerResult(LexerType.BINARY_LOGIC, "|", state)
            return None


class OperationBinaryAndMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None and previous_match in [
            LexerType.NUMBER,
            LexerType.IDENTIFIER,
        ]:
            if string[0] == "&":
                if string[1] == "&":
                    Logger.info("found: &&")
                    return LexerResult(LexerType.BINARY_LOGIC, "&&", state)
                else:
                    Logger.info("found: &")
                    return LexerResult(LexerType.BINARY_LOGIC, "&", state)
            return None


class OperationBinaryStringConcatenationMatcher(BaseOperatorMatcher):
    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None:
            Logger.info(f"previous: {previous_match.type}")
            if previous_match.type in [
                LexerType.NUMBER,
                LexerType.IDENTIFIER,
                LexerType.STRING,
            ]:
                if string[0] == "+":
                    Logger.info(f"found: {string[0]}")
                    return LexerResult(LexerType.BINARY_LOGIC, string[0], state)
        return None


# ternary: if-else (? :)
class OperationTernaryMatcher(BaseOperatorMatcher):

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | None:
        string = state.peek()
        if previous_match is not None:
            Logger.info(f"previous: {previous_match.type}")
            if previous_match.type in [
                LexerType.NUMBER,
                LexerType.IDENTIFIER,
                LexerType.STRING,
                LexerType.RESERVED_WORD,
            ]:
                if string[0] in ["?", ":"]:
                    Logger.info(f"found: {string[0]}")
                    return LexerResult(LexerType.TERNARY_LOGIC, string[0], state)
        return None


class OperationCalculationMatcher(BaseMatcher):
    def __init__(self) -> None:
        self._matchers: list[BaseMatcher] = []
        self._matchers.append(OperationUnaryNotOperatorMatcher())
        self._matchers.append(OperationUnaryIncrementOperatorMatcher())
        self._matchers.append(OperationUnaryDecrementOperatorMatcher())
        self._matchers.append(OperationUnaryNegationOperatorMatcher())

        self._matchers.append(OperationBinaryOperatorMatcher())
        self._matchers.append(OperationBinaryAssignmentMatcher())
        self._matchers.append(OperationBinaryNegativeComparisonMatcher())
        self._matchers.append(OperationBinaryGreaterComparisonMatcher())
        self._matchers.append(OperationBinaryLessorComparisonMatcher())
        self._matchers.append(OperationBinaryOrMatcher())
        self._matchers.append(OperationBinaryAndMatcher())
        self._matchers.append(OperationBinaryStringConcatenationMatcher())

        self._matchers.append(OperationTernaryMatcher())

    def try_match(
        self, state: LexerState, previous_match: LexerResult | None
    ) -> LexerResult | Error:
        Logger.info("calulation matcher")
        string = state.peek()
        if len(string) > 1:
            for matcher in self._matchers:
                result = matcher.try_match(state, previous_match)
                if result is not None:
                    return result
        Logger.info("not found")
        return None
