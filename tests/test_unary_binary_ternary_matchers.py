from unittest import TestCase

from purist.lexer.operation_unary_binary_ternary_matcher import (
    OperationUnaryNotOperatorMatcher,
)
from purist.models.lexer_models import LexerResult, LexerState, LexerType


# self._matchers.append(OperationUnaryNotOperatorMatcher())
# self._matchers.append(OperationUnaryIncrementOperatorMatcher())
# self._matchers.append(OperationUnaryDecrementOperatorMatcher())
# self._matchers.append(OperationUnaryNegationOperatorMatcher())

# self._matchers.append(OperationBinaryOperatorMatcher())
# self._matchers.append(OperationBinaryAssignmentMatcher())
# self._matchers.append(OperationBinaryNegativeComparisonMatcher())
# self._matchers.append(OperationBinaryGreaterComparisonMatcher())
# self._matchers.append(OperationBinaryLessorComparisonMatcher())
# self._matchers.append(OperationBinaryOrMatcher())
# self._matchers.append(OperationBinaryAndMatcher())
# self._matchers.append(OperationBinaryStringConcatenationMatcher())

# self._matchers.append(OperationTernaryMatcher())


class TestUnaryBinaryTernaryMatchers(TestCase):
    def test_unary_not_operator_matcher(self):
        # given
        text = "!b"
        state = LexerState("test", text)
        service = OperationUnaryNotOperatorMatcher()
        previous_match = LexerResult(
            LexerType.BINARY_LOGIC, "=", LexerState("test", "=")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.UNARY_LOGIC)
        self.assertEqual(result.value, "!")

    def test_unary_not_not_found_operator_matcher(self):
        # given
        text = "!b"
        state = LexerState("test", text)
        service = OperationUnaryNotOperatorMatcher()
        previous_match = LexerResult(LexerType.STRING, "=", LexerState("test", "="))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNone(result)
