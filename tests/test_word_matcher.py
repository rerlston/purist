from unittest import TestCase

from purist.lexer.word_matcher import WordMatcher
from purist.models.lexer_models import LexerResult, LexerType, LexerState
from purist.utils.logger import Logger, LogLevel


class TestLexer(TestCase):

    def setUp(self):
        Logger.configure(log_level=LogLevel.TRACE)

    def test_reserved_type_word(self):
        # given
        text = "type"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MODEL)

    def test_reserved_service_word(self):
        # given
        text = "service"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.SERVICE)

    def test_reserved_class_word(self):
        # given
        text = "class"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.SERVICE)

    def test_reserved_nodel_word(self):
        # given
        text = "model"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.MODEL)

    def test_reserved_interface_word(self):
        # given
        text = "interface"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.INTENT)

    def test_reserved_contract_word(self):
        # given
        text = "contract"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.INTENT)

    def test_reserved_portal_word(self):
        # given
        text = "portal"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.INTENT)

    def test_reserved_enumeration_word(self):
        # given
        text = "enumeration"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.ENUMERATION)

    def test_reserved_private_word(self):
        # given
        text = "private"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_public_word(self):
        # given
        text = "public"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_constructor_word(self):
        # given
        text = "constructor"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_destructor_word(self):
        # given
        text = "destructor"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_if_word(self):
        # given
        text = "if"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_while_word(self):
        # given
        text = "while"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_new_word(self):
        # given
        text = "new"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_int_word(self):
        # given
        text = "int"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_integer_word(self):
        # given
        text = "integer"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_decimal_word(self):
        # given
        text = "decimal"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_number_word(self):
        # given
        text = "number"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_string_word(self):
        # given
        text = "string"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_bool_word(self):
        # given
        text = "bool"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_boolean_word(self):
        # given
        text = "boolean"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_true_word(self):
        # given
        text = "true"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_false_word(self):
        # given
        text = "false"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_null_word(self):
        # given
        text = "null"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_or_word(self):
        # given
        text = "or"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_and_word(self):
        # given
        text = "and"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_not_word(self):
        # given
        text = "not"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_equal_word(self):
        # given
        text = "equal"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_greater_word(self):
        # given
        text = "greater"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_less_word(self):
        # given
        text = "less"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_is_word(self):
        # given
        text = "is"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_in_word(self):
        # given
        text = "in"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_self_word(self):
        # given
        text = "self"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_this_word(self):
        # given
        text = "this"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_abstract_word(self):
        # given
        text = "abstract"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BLUEPRINT)

    def test_reserved_concept_word(self):
        # given
        text = "concept"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BLUEPRINT)

    def test_reserved_conceptual_word(self):
        # given
        text = "conceptual"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BLUEPRINT)

    def test_reserved_theory_word(self):
        # given
        text = "theory"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BLUEPRINT)

    def test_reserved_theoretical_word(self):
        # given
        text = "theoretical"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BLUEPRINT)

    def test_reserved_virtual_word(self):
        # given
        text = "virtual"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_import_word(self):
        # given
        text = "import"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_from_word(self):
        # given
        text = "from"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_require_word(self):
        # given
        text = "require"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_implements_word(self):
        # given
        text = "implements"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.FULFILLS)

    def test_reserved_extends_word(self):
        # given
        text = "extends"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.BEHAVES_LIKE)

    def test_reserved_void_word(self):
        # given
        text = "void"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_reserved_print_word(self):
        # given
        text = "print"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.RESERVED_WORD)

    def test_constant_word(self):
        # given
        text = "MY_CONSTANT"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.CONSTANT)

    def test_identifier_word(self):
        # given
        text = "myVariableName"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.IDENTIFIER)

    def test_unknown_word(self):
        # given
        text = "a_b_c"
        state = LexerState("test", text)
        service = WordMatcher()

        # when
        result = service.try_match(state, None)

        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, LexerResult)
        self.assertEqual(result.type, LexerType.UNKNOWN)
