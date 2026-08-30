from unittest import TestCase
from unittest.mock import MagicMock

from purist.lexer.word_matcher import (
    ConstantKeywordMatcher,
    IdentifierKeywordMatcher,
    ReservedKeywordMatcher,
    WordMatcher,
)
from purist.models.lexer_models import LexerResult, TokenType
from purist.utils.logger import Logger, LogLevel


class TestWordMatcher(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.INFO)

    def test_reserved_type_word(self):
        # given
        text = "type"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.MODEL)

    def test_reserved_service_word(self):
        # given
        text = "service"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.SERVICE)

    def test_reserved_class_word(self):
        # given
        text = "class"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.SERVICE)

    def test_reserved_nodel_word(self):
        # given
        text = "model"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.MODEL)

    def test_reserved_interface_word(self):
        # given
        text = "interface"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.INTENT)

    def test_reserved_contract_word(self):
        # given
        text = "contract"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.INTENT)

    def test_reserved_portal_word(self):
        # given
        text = "portal"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.INTENT)

    def test_reserved_enumeration_word(self):
        # given
        text = "enumeration"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.ENUMERATION)

    def test_reserved_private_word(self):
        # given
        text = "private"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.PRIVATE)

    def test_reserved_public_word(self):
        # given
        text = "public"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.PUBLIC)

    def test_reserved_constructor_word(self):
        # given
        text = "constructor"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.CONSTRUCTOR)

    def test_reserved_destructor_word(self):
        # given
        text = "destructor"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.DESTRUCTOR)

    def test_reserved_if_word(self):
        # given
        text = "if"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.IF)

    def test_reserved_while_word(self):
        # given
        text = "while"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.WHILE)

    def test_reserved_new_word(self):
        # given
        text = "new"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.NEW)

    def test_reserved_int_word(self):
        # given
        text = "int"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.NUMBER_TYPE)

    def test_reserved_integer_word(self):
        # given
        text = "integer"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.NUMBER_TYPE)

    def test_reserved_decimal_word(self):
        # given
        text = "decimal"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.FLOAT_TYPE)

    def test_reserved_number_word(self):
        # given
        text = "number"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.FLOAT_TYPE)

    def test_reserved_string_word(self):
        # given
        text = "string"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.STRING_TYPE)

    def test_reserved_bool_word(self):
        # given
        text = "bool"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.BOOL_TYPE)

    def test_reserved_boolean_word(self):
        # given
        text = "boolean"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.BOOL_TYPE)

    def test_reserved_true_word(self):
        # given
        text = "true"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.TRUE)

    def test_reserved_false_word(self):
        # given
        text = "false"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.FALSE)

    def test_reserved_null_word(self):
        # given
        text = "null"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.NULL)

    def test_reserved_or_word(self):
        # given
        text = "or"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.LOGICAL_OR)

    def test_reserved_and_word(self):
        # given
        text = "and"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.LOGICAL_AND)

    def test_reserved_not_word(self):
        # given
        text = "not"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.LOGICAL_NOT)

    def test_reserved_equal_word(self):
        # given
        text = "equal"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.EQUALS)

    def test_reserved_greater_word(self):
        # given
        text = "greater"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.GREATER_THAN)

    def test_reserved_less_word(self):
        # given
        text = "less"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.LESS_THAN)

    def test_reserved_is_word(self):
        # given
        text = "is"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.IS)

    def test_reserved_in_word(self):
        # given
        text = "in"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.IN)

    def test_reserved_self_word(self):
        # given
        text = "self"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.THIS)

    def test_reserved_this_word(self):
        # given
        text = "this"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.THIS)

    def test_reserved_abstract_word(self):
        # given
        text = "abstract"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.BLUEPRINT)

    def test_reserved_concept_word(self):
        # given
        text = "concept"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.BLUEPRINT)

    def test_reserved_conceptual_word(self):
        # given
        text = "conceptual"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.BLUEPRINT)

    def test_reserved_theory_word(self):
        # given
        text = "theory"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.BLUEPRINT)

    def test_reserved_theoretical_word(self):
        # given
        text = "theoretical"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.BLUEPRINT)

    def test_reserved_protocol_word(self):
        # given
        text = "protocol"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.BLUEPRINT)

    def test_reserved_virtual_word(self):
        # given
        text = "virtual"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.VIRTUAL)

    def test_reserved_import_word(self):
        # given
        text = "import"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.IMPORT)

    def test_reserved_from_word(self):
        # given
        text = "from"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.FROM)

    def test_reserved_require_word(self):
        # given
        text = "require"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.REQUIRE)

    def test_reserved_implements_word(self):
        # given
        text = "implements"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.FULFILLS)

    def test_reserved_extends_word(self):
        # given
        text = "extends"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.BEHAVES_LIKE)

    def test_reserved_void_word(self):
        # given
        text = "void"
        state = MagicMock()
        service = ReservedKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.VOID)

    def test_constant_word(self):
        # given
        text = "MY_CONSTANT"
        state = MagicMock()
        service = ConstantKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.CONSTANT)

    def test_identifier_word(self):
        # given
        text = "myVariableName"
        state = MagicMock()
        service = IdentifierKeywordMatcher()

        # when
        result = service.try_match(text, state)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.IDENTIFIER)

    def test_detect_word(self):
        # given
        state = MagicMock()
        state.next_character.side_effect = [
            ("i", False),
            ("d", False),
            ("e", False),
            ("n", False),
            ("t", False),
            ("i", False),
            ("f", False),
            ("i", False),
            ("e", False),
            ("r", True),
        ]
        state.peek_next_character.return_value = "a", False
        expected_lexer_result = LexerResult(TokenType.IDENTIFIER, "identifier", state)
        mocked_identifier_matcher = MagicMock()
        mocked_identifier_matcher.try_match.return_value = expected_lexer_result
        matchers = []
        matchers.append(mocked_identifier_matcher)
        service = WordMatcher(matchers)

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.IDENTIFIER)
        self.assertEqual(result.value, "identifier")
        state.next_character.assert_called()

    def test_detect_unknown_word(self):
        # given
        state = MagicMock()
        state.next_character.side_effect = [
            ("i", False),
            ("d", False),
            ("e", False),
            ("n", False),
            ("t", False),
            ("i", False),
            ("f", False),
            ("i", False),
            ("e", False),
            ("r", True),
        ]
        state.peek_next_character.return_value = "a", False
        matchers = []
        service = WordMatcher(matchers)

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.UNKNOWN)
        self.assertEqual(result.value, "identifier")
        state.next_character.assert_called()

    def test_correct_word_extract(self):
        state = MagicMock()
        state.next_character.side_effect = [
            ("A", False),
            ("b", False),
            ("c", False),
            ("1", False),
            ("2", False),
            ("3", False),
            ("{", False),
            ("}", False),
        ]
        state.peek_next_character.return_value = "a", False
        matchers = []
        matchers.append(IdentifierKeywordMatcher())
        service = WordMatcher(matchers)

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, TokenType.IDENTIFIER)
        self.assertEqual(result.value, "Abc123")
        state.next_character.assert_called()
