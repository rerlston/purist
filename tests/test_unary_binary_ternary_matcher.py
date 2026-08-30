from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock

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
from purist.models.lexer_models import LexerResult, LexerType
from purist.utils.logger import Logger, LogLevel


class TestUnaryBinaryTernaryMatchers(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.INFO)

        self._mocked_state = MagicMock()
        self._mocked_previous_result = MagicMock()

    def test_unary_not_operator_matcher(self):
        # given
        text = "!"
        self._mocked_state.next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.ASSIGN)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationUnaryNotOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.LOGICAL_NOT)
        self.assertEqual(result.value, "!")
        self._mocked_state.next_character.assert_called_once()
        mocked_property.assert_called_once()

    def test_unary_not_found_operator_not_matcher(self):
        # given
        text = "!"
        self._mocked_state.next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationUnaryNotOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)
        self._mocked_state.next_character.assert_called_once()
        mocked_property.assert_called_once()

    def test_unary_not_operator_no_previous_not_matcher(self):
        # given
        text = "!"
        self._mocked_state.next_character.return_value = text, False
        service = OperationUnaryNotOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

    def test_unary_increment_operator_match(self):
        # given
        text = "+"
        self._mocked_state.next_character.side_effect = [(text, False), (text, False)]
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationUnaryIncrementOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.INCREMENT)
        self.assertEqual(result.value, "++")
        self.assertEqual(self._mocked_state.next_character.call_count, 2)
        self._mocked_state.peek_next_character.assert_called_once()

    def test_unary_increment_operator_not_match(self):
        # given
        text = "+"
        self._mocked_state.next_character.side_effect = [(text, False), (text, False)]
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationUnaryIncrementOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)
        self._mocked_state.next_character.assert_called_once()
        self._mocked_state.peek_next_character.assert_called_once()

    def test_unary_increment_operator_no_previous_not_match(self):
        # given
        self._mocked_state.next_character.return_value = None, True
        service = OperationUnaryIncrementOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)
        self.assertEqual(self._mocked_state.next_character.call_count, 0)

    def test_unary_decrement_operator_match(self):
        # given
        text = "-"
        self._mocked_state.next_character.side_effect = [(text, False), (text, False)]
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationUnaryDecrementOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.DECREMENT)
        self.assertEqual(result.value, "--")
        self.assertEqual(self._mocked_state.next_character.call_count, 2)
        self._mocked_state.peek_next_character.assert_called_once()

    def test_unary_decrement_operator_not_match(self):
        # given
        text = "-"
        self._mocked_state.next_character.side_effect = [(text, False), (text, False)]
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationUnaryDecrementOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)
        self._mocked_state.next_character.assert_called_once()
        self._mocked_state.peek_next_character.assert_called_once()

    def test_unary_decrement_operator_no_previous_not_match(self):
        # given
        self._mocked_state.next_character.return_value = None, True
        service = OperationUnaryDecrementOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)
        self.assertEqual(self._mocked_state.next_character.call_count, 0)

    def test_unary_negation_after_assignment_operator_match(self):
        # given
        text = "-"
        self._mocked_state.next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.ASSIGN)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationUnaryNegationOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NEGATION)
        self.assertEqual(result.value, "-")
        self._mocked_state.next_character.assert_called_once()

    def test_unary_negation_after_round_bracket_operator_match(self):
        # given
        text = "-"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.L_ROUND)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationUnaryNegationOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NEGATION)
        self.assertEqual(result.value, "-")
        self._mocked_state.next_character.assert_called_once()

    def test_unary_negation_operator_not_match(self):
        # given
        text = "-"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationUnaryNegationOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)
        self._mocked_state.next_character.assert_called_once()

    def test_unary_negation_operator_no_previous_not_match(self):
        # given
        service = OperationUnaryNegationOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

    def test_binary_addition_operator_after_identifier_match(self):
        # given
        text = "+"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.ADDITION)
        self.assertEqual(result.value, "+")
        self._mocked_state.next_character.assert_called_once()

    def test_binary_addition_operator_after_number_match(self):
        # given a = 2 + b
        text = "+"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.ADDITION)
        self.assertEqual(result.value, "+")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_subtraction_operator_after_identifier_match(self):
        # given a = b - 2
        text = "-"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.SUBTRACTION)
        self.assertEqual(result.value, "-")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_subtraction_operator_after_number_match(self):
        # given a = 2 - b
        text = "-"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.SUBTRACTION)
        self.assertEqual(result.value, "-")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_mod_operator_after_identifier_match(self):
        # given a = b % 2
        text = "%"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MOD)
        self.assertEqual(result.value, "%")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_mod_operator_after_number_match(self):
        # given a = 2 % b
        text = "%"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MOD)
        self.assertEqual(result.value, "%")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_xor_operator_after_identifier_match(self):
        # given a = b ^ 2
        text = "^"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.XOR)
        self.assertEqual(result.value, "^")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_xor_operator_after_number_match(self):
        # given a = 2 ^ b
        text = "^"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.XOR)
        self.assertEqual(result.value, "^")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_division_operator_after_identifier_match(self):
        # given a = b / 3
        text = "/"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = " ", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.DIVIDE)
        self.assertEqual(result.value, "/")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_division_operator_after_number_match(self):
        # given a = 2 / b
        text = "/"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = " ", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.DIVIDE)
        self.assertEqual(result.value, "/")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_multiplication_operator_after_identifier_match(self):
        # given a = b * 3
        text = "*"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = "3", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MULTIPLY)
        self.assertEqual(result.value, "*")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_multiplication_operator_after_number_match(self):
        # given a = 2 * b
        text = "*"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MULTIPLY)
        self.assertEqual(result.value, "*")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_power_operator_after_identifier_match(self):
        # given a = b ** 3
        text = "*"
        self._mocked_state.next_character.side_effect = [(text, False), (text, False)]
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.POWER)
        self.assertEqual(result.value, "**")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_power_operator_after_number_match(self):
        # given a = 2 ** b
        text = "*"
        self._mocked_state.next_character.side_effect = [(text, False), (text, False)]
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.POWER)
        self.assertEqual(result.value, "**")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_substraction_operator_no_previous_not_match(self):
        # given
        text = "-"
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

        self.assertEqual(self._mocked_state.next_character.call_count, 0)

    def test_binary_addition_operator_after_reserved_word_match(self):
        # given
        text = "+"
        self._mocked_state.next_character.side_effect = [(text, False), (text, False)]
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.PRIVATE)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)

        self._mocked_state.next_character.assert_called_once()

    def test_binary_assignment_operator_after_identifier_match(self):
        # given a = b / 3
        text = "="
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryAssignmentMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.ASSIGN)
        self.assertEqual(result.value, "=")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_assignment_operator_after_number_match(self):
        # given 1 = 2 / b
        text = "="
        self._mocked_state.next_character.return_value = text, False
        self._mocked_state.peek_next_character.return_value = text, False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryMathsOperatorMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)
        self.assertEqual(self._mocked_state.next_character.call_count, 1)

    def test_binary_not_equal_operator_after_identifier_match(self):
        # given a != b
        self._mocked_state.next_character.side_effect = [("!", False), ("=", False)]
        self._mocked_state.peek_next_character.return_value = "=", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryNegativeComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NOT_EQUALS)
        self.assertEqual(result.value, "!=")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_not_equal_operator_after_number_match(self):
        # given 1 != b
        self._mocked_state.next_character.side_effect = [("!", False), ("=", False)]
        self._mocked_state.peek_next_character.return_value = "=", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryNegativeComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.NOT_EQUALS)
        self.assertEqual(result.value, "!=")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_not_equal_operator_no_previous_not_match(self):
        # given != b
        self._mocked_state.next_character.side_effect = [("!", False), ("=", False)]
        self._mocked_state.peek_next_character.return_value = "=", False
        service = OperationBinaryNegativeComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

    def test_binary_greater_operator_after_identifier_match(self):
        # given a > b
        self._mocked_state.next_character.return_value = ">", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GREATER_THAN)
        self.assertEqual(result.value, ">")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_greater_operator_after_number_match(self):
        # given 1 > b
        text = ">"
        self._mocked_state.next_character.return_value = ">", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GREATER_THAN)
        self.assertEqual(result.value, ">")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_greater_equal_operator_after_identifier_match(self):
        # given a >= b
        self._mocked_state.next_character.side_effect = [(">", False), ("=", False)]
        self._mocked_state.peek_next_character.return_value = "=", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GREATER_OR_EQUAL)
        self.assertEqual(result.value, ">=")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_greater_equal_operator_after_number_not_match(self):
        # given 1 >= b
        self._mocked_state.next_character.side_effect = [(">", False), ("=", False)]
        self._mocked_state.peek_next_character.return_value = "=", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.GREATER_OR_EQUAL)
        self.assertEqual(result.value, ">=")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_greater_operator_no_previous_not_match(self):
        # given > b
        self._mocked_state.next_character.return_value = ">", False
        self._mocked_state.peek_next_character.return_value = "=", False
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

    def test_binary_lessor_operator_after_identifier_match(self):
        # given a < b
        self._mocked_state.next_character.return_value = "<", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryLessorComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.LESS_THAN)
        self.assertEqual(result.value, "<")

        self.assertEqual(self._mocked_state.next_character.call_count, 1)

    def test_binary_lessor_operator_after_number_match(self):
        # given 1 < b
        self._mocked_state.next_character.return_value = "<", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryLessorComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.LESS_THAN)
        self.assertEqual(result.value, "<")

        self.assertEqual(self._mocked_state.next_character.call_count, 1)

    def test_binary_lessor_equal_operator_after_identifier_match(self):
        # given a <= b
        self._mocked_state.next_character.side_effect = [("<", False), ("=", False)]
        self._mocked_state.peek_next_character.return_value = "=", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryLessorComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.LESS_OR_EQUAL)
        self.assertEqual(result.value, "<=")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_lessor_equal_operator_after_number_match(self):
        # given 1 <= b
        self._mocked_state.next_character.side_effect = [("<", False), ("=", False)]
        self._mocked_state.peek_next_character.return_value = "=", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryLessorComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.LESS_OR_EQUAL)
        self.assertEqual(result.value, "<=")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_lessor_operator_no_previous_not_match(self):
        # given < b
        self._mocked_state.next_character.return_value = "<", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryLessorComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

    def test_binary_or_calculation_operator_after_identifier_match(self):
        # given a | b
        self._mocked_state.next_character.return_value = "|", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryOrMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MATH_OR)
        self.assertEqual(result.value, "|")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_or_calculation_operator_after_number_match(self):
        # given 1 | b
        self._mocked_state.next_character.return_value = "|", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryOrMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MATH_OR)
        self.assertEqual(result.value, "|")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_or_boolean_operator_after_identifier_match(self):
        # given a || b
        self._mocked_state.next_character.side_effect = [("|", False), ("|", False)]
        self._mocked_state.peek_next_character.return_value = "|", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryOrMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.LOGICAL_OR)
        self.assertEqual(result.value, "||")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_or_boolean_operator_after_number_match(self):
        # given 1 || b
        self._mocked_state.next_character.side_effect = [("|", False), ("|", False)]
        self._mocked_state.peek_next_character.return_value = "|", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryOrMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.LOGICAL_OR)
        self.assertEqual(result.value, "||")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_or_maths_operator_no_previous_not_match(self):
        # given | b
        self._mocked_state.next_character.return_value = "|", False
        self._mocked_state.peek_next_character.return_value = "b", False
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)
        self.assertEqual(self._mocked_state.next_character.call_count, 0)

    def test_binary_or_boolean_operator_no_previous_not_match(self):
        # given || b
        self._mocked_state.next_character.side_effect = [("|", False), ("|", False)]
        self._mocked_state.peek_next_character.return_value = "|", False
        service = OperationBinaryGreaterComparisonMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)
        self.assertEqual(self._mocked_state.next_character.call_count, 0)

    # self._matchers.append(OperationBinaryAndMatcher())
    def test_binary_and_calculation_operator_after_identifier_match(self):
        # given a & b
        self._mocked_state.next_character.return_value = "&", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryAndMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MATH_AND)
        self.assertEqual(result.value, "&")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_and_calculation_operator_after_number_match(self):
        # given 1 & b
        self._mocked_state.next_character.return_value = "&", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryAndMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MATH_AND)
        self.assertEqual(result.value, "&")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_and_boolean_operator_after_identifier_match(self):
        # given a && b
        self._mocked_state.next_character.side_effect = [("&", False), ("&", False)]
        self._mocked_state.peek_next_character.return_value = "&", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryAndMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.LOGICAL_AND)
        self.assertEqual(result.value, "&&")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_and_boolean_operator_after_number_not_match(self):
        # given 1 && b
        self._mocked_state.next_character.side_effect = [("&", False), ("&", False)]
        self._mocked_state.peek_next_character.return_value = "&", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryAndMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.LOGICAL_AND)
        self.assertEqual(result.value, "&&")

        self.assertEqual(self._mocked_state.next_character.call_count, 2)

    def test_binary_and_maths_operator_no_previous_not_match(self):
        # given & b
        self._mocked_state.next_character.return_value = "&", False
        self._mocked_state.peek_next_character.return_value = "&", False
        service = OperationBinaryAndMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

        self.assertEqual(self._mocked_state.next_character.call_count, 0)

    def test_binary_and_boolean_operator_no_previous_not_match(self):
        # given && b
        self._mocked_state.next_character.side_effect = [("&", False), ("&", False)]
        self._mocked_state.peek_next_character.return_value = "&", False
        service = OperationBinaryAndMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

        self.assertEqual(self._mocked_state.next_character.call_count, 0)

    def test_binary_identity_concatenation_operator_after_string_match(self):
        # given "string" + b
        self._mocked_state.next_character.return_value = "+", False
        self._mocked_state.peek_next_character.return_value = "b", False
        mocked_property = PropertyMock(return_value=LexerType.STRING_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryStringConcatenationMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.STRING_CONCATENATION)
        self.assertEqual(result.value, "+")

        self._mocked_state.next_character.assert_called_once()

    def test_binary_string_concatenation_operator_after_number_no_match(self):
        # given "1 + string"
        self._mocked_state.next_character.return_value = "+", False
        self._mocked_state.peek_next_character.return_value = "s", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationBinaryStringConcatenationMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)

    # everything below this line needs to be updated to use mocks

    def test_binary_string_concatenation_operator_no_previous_match(self):
        # given + "sting"
        self._mocked_state.next_character.return_value = "+", False
        self._mocked_state.peek_next_character.return_value = "s", False
        service = OperationBinaryStringConcatenationMatcher()

        # when
        result = service.try_match(self._mocked_state, None)

        # then
        self.assertIsNone(result)

    def test_ternary_first_part_concatenation_operator_after_number_match(self):
        # given a = 1==1 ? c : d
        self._mocked_state.next_character.return_value = "?", False
        self._mocked_state.peek_next_character.return_value = "c", False
        mocked_property = PropertyMock(return_value=LexerType.NUMBER_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationTernaryMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.QUESTION)
        self.assertEqual(result.value, "?")

    def test_ternary_first_part_concatenation_operator_after_string_match(self):
        # given a = b=="" ? c : d
        self._mocked_state.next_character.return_value = "?", False
        self._mocked_state.peek_next_character.return_value = "c", False
        mocked_property = PropertyMock(return_value=LexerType.STRING_LITERAL)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationTernaryMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.QUESTION)
        self.assertEqual(result.value, "?")

    def test_ternary_first_part_concatenation_operator_after_identifier_match(self):
        # given a = 1==b ? c : d
        self._mocked_state.next_character.return_value = "?", False
        self._mocked_state.peek_next_character.return_value = "c", False
        mocked_property = PropertyMock(return_value=LexerType.IDENTIFIER)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationTernaryMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.QUESTION)
        self.assertEqual(result.value, "?")

    def test_ternary_first_part_concatenation_operator_after_boolean_match(self):
        # given a = b == true ? c : d
        self._mocked_state.next_character.return_value = "?", False
        self._mocked_state.peek_next_character.return_value = "c", False
        mocked_property = PropertyMock(return_value=LexerType.TRUE)
        type(self._mocked_previous_result).type = mocked_property
        service = OperationTernaryMatcher()

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.QUESTION)
        self.assertEqual(result.value, "?")

    def test_operation_calculation_matcher_list_of_matchers(self):
        # given
        operator_matchers = []
        mocked_base_operator = MagicMock()
        mocked_base_operator.try_match.return_value = LexerResult(
            LexerType.ADDITION, "+", self._mocked_state
        )
        operator_matchers.append(mocked_base_operator)
        service = OperationCalculationMatcher(operator_matchers)

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNotNone(result)
        self.assertEqual(mocked_base_operator.try_match.call_count, 1)

    def test_operation_calculation_matcher_no_list_of_matchers(self):
        # given
        operator_matchers = []
        service = OperationCalculationMatcher(operator_matchers)

        # when
        result = service.try_match(self._mocked_state, self._mocked_previous_result)

        # then
        self.assertIsNone(result)
