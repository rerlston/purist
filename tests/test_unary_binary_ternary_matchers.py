from unittest import TestCase

from purist.lexer.operation_unary_binary_ternary_matcher import (
    OperationBinaryAndMatcher,
    OperationBinaryAssignmentMatcher,
    OperationBinaryGreaterComparisonMatcher,
    OperationBinaryLessorComparisonMatcher,
    OperationBinaryNegativeComparisonMatcher,
    OperationBinaryMathsOperatorMatcher,
    OperationBinaryOrMatcher,
    OperationBinaryStringConcatenationMatcher,
    OperationCalculationMatcher,
    OperationTernaryMatcher,
    OperationUnaryDecrementOperatorMatcher,
    OperationUnaryIncrementOperatorMatcher,
    OperationUnaryNegationOperatorMatcher,
    OperationUnaryNotOperatorMatcher,
)
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.logger import Logger, LogLevel


class TestUnaryBinaryTernaryMatchers(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.TRACE)

    def test_unary_not_operator_matcher(self):
        # given
        text = "!b"
        state = LexerState("test", text)
        service = OperationUnaryNotOperatorMatcher()
        previous_match = LexerResult(
            LexerType.BINARY_LOGIC, "=", LexerState("test", "=!b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.UNARY_LOGIC)
        self.assertEqual(result.value, "!")

    def test_unary_not_found_operator_not_matcher(self):
        # given
        text = "!b"
        state = LexerState("test", text)
        service = OperationUnaryNotOperatorMatcher()
        previous_match = LexerResult(LexerType.STRING, "=", LexerState("test", "=!b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNone(result)

    def test_unary_not_operator_no_previous_not_matcher(self):
        # given
        text = "!b"
        state = LexerState("test", text)
        service = OperationUnaryNotOperatorMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_unary_increment_operator_match(self):
        # given
        text = "++"
        state = LexerState("test", text)
        service = OperationUnaryIncrementOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b++")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.UNARY_LOGIC)
        self.assertEqual(result.value, "++")

    def test_unary_increment_operator_not_match(self):
        # given
        text = "++"
        state = LexerState("test", text)
        service = OperationUnaryIncrementOperatorMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "1", LexerState("test", "1++"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNone(result)

    def test_unary_increment_operator_no_previous_not_match(self):
        # given
        text = "++"
        state = LexerState("test", text)
        service = OperationUnaryIncrementOperatorMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_unary_decrement_operator_match(self):
        # given
        text = "--"
        state = LexerState("test", text)
        service = OperationUnaryDecrementOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b--")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.UNARY_LOGIC)
        self.assertEqual(result.value, "--")

    def test_unary_decrement_operator_not_match(self):
        # given
        text = "--"
        state = LexerState("test", text)
        service = OperationUnaryDecrementOperatorMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "1", LexerState("test", "1--"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNone(result)

    def test_unary_decrement_operator_no_previous_not_match(self):
        # given
        text = "--"
        state = LexerState("test", text)
        service = OperationUnaryDecrementOperatorMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_unary_negation_after_assignment_operator_match(self):
        # given
        text = "-b"
        state = LexerState("test", text)
        service = OperationUnaryNegationOperatorMatcher()
        previous_match = LexerResult(
            LexerType.BINARY_LOGIC, "=", LexerState("test", "= -b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.UNARY_LOGIC)
        self.assertEqual(result.value, "-")

    def test_unary_negation_after_round_bracket_operator_match(self):
        # given
        text = "-1"
        state = LexerState("test", text)
        service = OperationUnaryNegationOperatorMatcher()
        previous_match = LexerResult(
            LexerType.BINARY_LOGIC, "(", LexerState("test", "(-1)")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.UNARY_LOGIC)
        self.assertEqual(result.value, "-")

    def test_unary_negation_operator_not_match(self):
        # given
        text = "-1"
        state = LexerState("test", text)
        service = OperationUnaryNegationOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b-1")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNone(result)

    def test_unary_negation_operator_no_previous_not_match(self):
        # given
        text = "-1"
        state = LexerState("test", text)
        service = OperationUnaryNegationOperatorMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_binary_addition_operator_after_identifier_match(self):
        # given a = b + 2
        text = "+ 2"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b + 2")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "+")

    def test_binary_addition_operator_after_number_match(self):
        # given a = 2 + b
        text = "+ b"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "2", LexerState("test", "2 + b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "+")

    def test_binary_subtraction_operator_after_identifier_match(self):
        # given a = b - 2
        text = "- 2"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b - 2")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "-")

    def test_binary_subtraction_operator_after_number_match(self):
        # given a = 2 - b
        text = "- b"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "2", LexerState("test", "2 - b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "-")

    def test_binary_mod_operator_after_identifier_match(self):
        # given a = b % 2
        text = "% 2"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b % 2")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "%")

    def test_binary_mod_operator_after_number_match(self):
        # given a = 2 % b
        text = "% b"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "2", LexerState("test", "2 % b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "%")

    def test_binary_xor_operator_after_identifier_match(self):
        # given a = b ^ 2
        text = "^ 2"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b ^ 2")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "^")

    def test_binary_xor_operator_after_number_match(self):
        # given a = 2 ^ b
        text = "^ b"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "2", LexerState("test", "2 ^ b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "^")

    def test_binary_division_operator_after_identifier_match(self):
        # given a = b / 3
        text = "/3"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b/3")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "/")

    def test_binary_division_operator_after_number_match(self):
        # given a = 2 / b
        text = "/ b"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "2", LexerState("test", "2 / b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "/")

    def test_binary_multiplication_operator_after_identifier_match(self):
        # given a = b * 3
        text = "*3"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b*3")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "*")

    def test_binary_multiplication_operator_after_number_match(self):
        # given a = 2 * b
        text = "* b"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "2", LexerState("test", "2 * b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "*")

    def test_binary_power_operator_after_identifier_match(self):
        # given a = b ** 3
        text = "**3"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b**3")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "**")

    def test_binary_power_operator_after_number_match(self):
        # given a = 2 ** b
        text = "** b"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(
            LexerType.NUMBER, "2", LexerState("test", "2 ** b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "**")

    def test_binary_substraction_operator_no_previous_not_match(self):
        # given
        text = "- a"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_binary_addition_operator_after_reserved_word_not_match(self):
        # given
        text = "+ a"
        state = LexerState("test", text)
        service = OperationBinaryMathsOperatorMatcher()
        previous_match = LexerResult(
            LexerType.RESERVED_WORD, "interface", LexerState("test", "interface + a")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNone(result)

    def test_binary_assignment_operator_after_identifier_match(self):
        # given a = b / 3
        text = "= b / 3"
        state = LexerState("test", text)
        service = OperationBinaryAssignmentMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a=b / 3")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "=")

    def test_binary_assignment_operator_after_number_not_match(self):
        # given 1 = 2 / b
        text = "= / b"
        state = LexerState("test", text)
        service = OperationBinaryAssignmentMatcher()
        previous_match = LexerResult(
            LexerType.NUMBER, "1", LexerState("test", "1 = 2 / b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNone(result)

    def test_binary_not_equal_operator_after_identifier_match(self):
        # given a != b
        text = "!= b"
        state = LexerState("test", text)
        service = OperationBinaryNegativeComparisonMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a != b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "!=")

    def test_binary_not_equal_operator_after_number_not_match(self):
        # given 1 != b
        text = "!= b"
        state = LexerState("test", text)
        service = OperationBinaryNegativeComparisonMatcher()
        previous_match = LexerResult(
            LexerType.NUMBER, "1", LexerState("test", "1 != b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "!=")

    def test_binary_not_equal_operator_no_previous_not_match(self):
        # given != b
        text = "!= b"
        state = LexerState("test", text)
        service = OperationBinaryNegativeComparisonMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_binary_greater_operator_after_identifier_match(self):
        # given a > b
        text = "> b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a > b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, ">")

    def test_binary_greater_operator_after_number_not_match(self):
        # given 1 > b
        text = "> b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "1", LexerState("test", "1 > b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, ">")

    def test_binary_greater_equal_operator_after_identifier_match(self):
        # given a >= b
        text = ">= b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a >= b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, ">=")

    def test_binary_greater_equal_operator_after_number_not_match(self):
        # given 1 >= b
        text = ">= b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()
        previous_match = LexerResult(
            LexerType.NUMBER, "1", LexerState("test", "1 >= b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, ">=")

    def test_binary_greater_operator_no_previous_not_match(self):
        # given > b
        text = "> b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_binary_lessor_operator_after_identifier_match(self):
        # given a < b
        text = "< b"
        state = LexerState("test", text)
        service = OperationBinaryLessorComparisonMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a < b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "<")

    def test_binary_lessor_operator_after_number_not_match(self):
        # given 1 < b
        text = "< b"
        state = LexerState("test", text)
        service = OperationBinaryLessorComparisonMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "1", LexerState("test", "1 < b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "<")

    def test_binary_lessor_equal_operator_after_identifier_match(self):
        # given a <= b
        text = "<= b"
        state = LexerState("test", text)
        service = OperationBinaryLessorComparisonMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a <= b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "<=")

    def test_binary_lessor_equal_operator_after_number_not_match(self):
        # given 1 <= b
        text = "<= b"
        state = LexerState("test", text)
        service = OperationBinaryLessorComparisonMatcher()
        previous_match = LexerResult(
            LexerType.NUMBER, "1", LexerState("test", "1 <= b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "<=")

    def test_binary_lessor_operator_no_previous_not_match(self):
        # given < b
        text = "< b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_binary_or_calculation_operator_after_identifier_match(self):
        # given a | b
        text = "| b"
        state = LexerState("test", text)
        service = OperationBinaryOrMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a | b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "|")

    def test_binary_or_calculation_operator_after_number_not_match(self):
        # given 1 | b
        text = "| b"
        state = LexerState("test", text)
        service = OperationBinaryOrMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "1", LexerState("test", "1 | b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "|")

    def test_binary_or_boolean_operator_after_identifier_match(self):
        # given a || b
        text = "|| b"
        state = LexerState("test", text)
        service = OperationBinaryOrMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a || b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "||")

    def test_binary_or_boolean_operator_after_number_not_match(self):
        # given 1 || b
        text = "|| b"
        state = LexerState("test", text)
        service = OperationBinaryOrMatcher()
        previous_match = LexerResult(
            LexerType.NUMBER, "1", LexerState("test", "1 || b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "||")

    def test_binary_or_maths_operator_no_previous_not_match(self):
        # given | b
        text = "| b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_binary_or_boolean_operator_no_previous_not_match(self):
        # given || b
        text = "|| b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    # self._matchers.append(OperationBinaryAndMatcher())
    def test_binary_and_calculation_operator_after_identifier_match(self):
        # given a & b
        text = "& b"
        state = LexerState("test", text)
        service = OperationBinaryAndMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a & b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "&")

    def test_binary_and_calculation_operator_after_number_not_match(self):
        # given 1 & b
        text = "& b"
        state = LexerState("test", text)
        service = OperationBinaryAndMatcher()
        previous_match = LexerResult(LexerType.NUMBER, "1", LexerState("test", "1 & b"))

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "&")

    def test_binary_and_boolean_operator_after_identifier_match(self):
        # given a && b
        text = "&& b"
        state = LexerState("test", text)
        service = OperationBinaryAndMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "a", LexerState("test", "a && b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "&&")

    def test_binary_and_boolean_operator_after_number_not_match(self):
        # given 1 && b
        text = "&& b"
        state = LexerState("test", text)
        service = OperationBinaryAndMatcher()
        previous_match = LexerResult(
            LexerType.NUMBER, "1", LexerState("test", "1 && b")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BINARY_LOGIC)
        self.assertEqual(result.value, "&&")

    def test_binary_and_maths_operator_no_previous_not_match(self):
        # given & b
        text = "& b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_binary_and_boolean_operator_no_previous_not_match(self):
        # given && b
        text = "&& b"
        state = LexerState("test", text)
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    def test_binary_identity_concatenation_operator_after_string_match(self):
        # given "string" + b
        text = "+ b"
        state = LexerState("test", text)
        service = OperationBinaryStringConcatenationMatcher()
        previous_match = LexerResult(
            LexerType.STRING, '"string"', LexerState("test", '"string" + b')
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.STRING_CONCATENATION)
        self.assertEqual(result.value, "+")

    def test_binary_string_concatenation_operator_after_number_no_match(self):
        # given "1 + string"
        text = '+ "string"'
        state = LexerState("test", text)
        service = OperationBinaryStringConcatenationMatcher()
        previous_match = LexerResult(
            LexerType.NUMBER, "1", LexerState("test", '1 + "string"')
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNone(result)

    def test_binary_string_concatenation_operator_no_previous_match(self):
        # given + "sting"
        text = '+ "string"'
        state = LexerState("test", text)
        service = OperationBinaryStringConcatenationMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNone(result)

    # self._matchers.append(OperationTernaryMatcher())
    def test_ternary_first_part_concatenation_operator_after_number_match(self):
        # given a = 1==1 ? c : d
        text = "? c : d"
        state = LexerState("test", text)
        service = OperationTernaryMatcher()
        previous_match = LexerResult(
            LexerType.NUMBER, "1", LexerState("test", "1==1 ? c : d")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.TERNARY_LOGIC)
        self.assertEqual(result.value, "?")

    def test_ternary_first_part_concatenation_operator_after_string_match(self):
        # given a = b=="" ? c : d
        text = "? c : d"
        state = LexerState("test", text)
        service = OperationTernaryMatcher()
        previous_match = LexerResult(
            LexerType.STRING, "", LexerState("test", '"" ? c : d')
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.TERNARY_LOGIC)
        self.assertEqual(result.value, "?")

    def test_ternary_first_part_concatenation_operator_after_identifier_match(self):
        # given a = 1==b ? c : d
        text = "? c : d"
        state = LexerState("test", text)
        service = OperationTernaryMatcher()
        previous_match = LexerResult(
            LexerType.IDENTIFIER, "b", LexerState("test", "b ? c : d")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.TERNARY_LOGIC)
        self.assertEqual(result.value, "?")

    def test_ternary_first_part_concatenation_operator_after_boolean_match(self):
        # given a = b == true ? c : d
        text = "? c : d"
        state = LexerState("test", text)
        service = OperationTernaryMatcher()
        previous_match = LexerResult(
            LexerType.BOOLEAN_VALUE, "true", LexerState("test", "true ? c : d")
        )

        # when
        result = service.try_match(state, previous_match)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.TERNARY_LOGIC)
        self.assertEqual(result.value, "?")
