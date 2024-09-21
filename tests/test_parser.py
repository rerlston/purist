from unittest import TestCase, mock

from parser import Parser


class TestParser(TestCase):
    def test_parse_empty_class_definition(self):
        # given
        code = 'class A {\n}'

        file_reader = mock.MagicMock()
        file_reader.read.return_value = code
        service = Parser('test', file_reader)

        # when
        try:
            ast = service.parse('test1.purist')
        except Exception as e:
            self.fail(e)

        # then
        file_reader.read.assert_called_once_with("test/test1.purist")
        self.assertIsNotNone(ast)
        if ast is not None:
            self.assertIsNotNone(ast.children)
        if ast is not None and ast.children is not None:
            self.assertEqual(1, len(ast.children))

    def test_class_with_extends(self):
        # given
        code = 'class A extends B {\n}'

        file_reader = mock.MagicMock()
        file_reader.read.return_value = code
        service = Parser('test', file_reader)

        # when
        try:
            ast = service.parse('test2.purist')
        except Exception as e:
            self.fail(e)

        # then
        file_reader.read.assert_called_once_with("test/test2.purist")
        self.assertIsNotNone(ast)
        if ast is not None:
            self.assertIsNotNone(ast.children)
        if ast is not None and ast.children is not None:
            self.assertEqual(1, len(ast.children))
