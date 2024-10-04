"""
Purist Parser, entry point to parse the purist source code
"""
import json
import logging
import re
import sys

from os import environ as env
from os.path import join as path

import time
from typing import Any, Dict, List, Tuple
from errors import InvalidClassName, InvalidImportStatement, InvalidInterfaceName, InvalidMethodName, InvalidVariableName, UnexpectedKeyword
from tokenizer import Token, TokenType, Tokenizer

PASCAL_CASE = r'^[A-Z](([a-zA-Z0-9]+[A-Z]?)*)$'
CLASS_CASE = PASCAL_CASE
INTERFACE_CASE = PASCAL_CASE
CAMEL_CASE = r'^[a-z]|([A-Z0-9])[a-z]*'
METHOD_CASE = CAMEL_CASE
VARIABLE_CASE = CAMEL_CASE
CONSTANT = r'^[A-Z][A-Z0-9_][A-Z]+$'


class Node():
    """
    Abstract Syntax Tree Node
    """

    def __init__(self, node_name: str, value: str | int | float | None = None) -> None:
        self._node_name = node_name
        self._value = value
        self._children: 'List[Node]|None' = None

    @property
    def children(self) -> 'List[Node]|None':
        """
        Returns the children of the node
        """
        return self._children

    def add_child(self, node: 'Node|None') -> None:
        """
        Adds a child to the parent (current) node
        Args:
            node: the node to add as a child
        """
        if node is not None:
            if self._children is None:
                self._children = []
            self._children.append(node)

    @property
    def value(self) -> str | int | float | None:
        """
        Returns the value of the node

        Returns:
            str|int|float|None: the value of the node
        """
        return self._value

    @value.setter
    def value(self, value: str | int | float) -> None:
        self._value = value

    def __repr__(self) -> str:
        response: Dict[str, Any] = {}
        response['type'] = self._node_name
        if self._value is not None:
            response['value'] = self._value
        if self._children is not None:
            children: List[Dict[str, Any]] = []
            for child in self._children:
                children.append(json.loads(child.__repr__()))
            response['children'] = children
        return json.dumps(response, indent=4)

class FileReader:
    def read(self, filename: str) -> str:
        with open(filename, 'r') as f:
            return f.read()

class Parser():
    """
    Purist Parser, once it has tokens it checks if the tokens can form a valid AST
    """

    def __init__(self, src_folder: str, file_reader: FileReader) -> None:
        self._tokenizer = Tokenizer()
        self._src_folder = src_folder
        self._file_reader = file_reader
        self._parsed_files: List[str] = []
        self._parsed_file_nodes: Dict[str, Node] = {}

    def parse(self, file_path: str) -> Node | None:
        """
        Parse a file and return a root Node of the AST

        Args:
            file_path: path to the file to parse
        Returns:
            Node: an abstract syntax tree root node
        """
        if file_path in self._parsed_files:
            if file_path in self._parsed_file_nodes:
                print(f'parsing {file_path} from cache')
                return self._parsed_file_nodes[file_path]
            print("cyclic dependency detected")
            return None
        full_path = path(self._src_folder, file_path)
        print(f'parsing {full_path}')
        try:
            self._parsed_files.append(file_path)
            text = self._file_reader.read(full_path)
            tokens = self._tokenizer.tokenize(file_path, text)
            ast = self._parse_tokens(tokens, file_path)
            self._parsed_file_nodes[file_path] = ast
            return ast
        except FileNotFoundError:
            print(f'File not found: {full_path}')
            error = InvalidImportStatement(full_path, 0, 0)
            raise ValueError(error.get_error())
        except RecursionError:
            print('Recursion error')
            error = InvalidImportStatement(full_path, 0, 0)
            raise ValueError(error.get_error())
        except ValueError as e:
            print(e)
            return None

    def _parse_tokens(self, tokens: List[Token], filename: str) -> Node:
        token_index = 0
        filename = filename[:-7]
        filename = filename.replace('/', '.')
        root_node: Node = Node('source', filename)
        while token_index < len(tokens):
            token = tokens[token_index]
            if token.type == TokenType.FROM:
                nodes, token_index = self._parse_import_statements(tokens, token_index)
                for node in nodes:
                    root_node.add_child(node)
            elif token.type == TokenType.CLASS:
                node, token_index = self._parse_class(tokens, token_index)
                root_node.add_child(node)
            else:
                token_index += 1
        return root_node

    def _parse_class_identifier(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        current_token = tokens[index]
        if current_token.type == TokenType.IDENTIFIER:
            class_name = str(current_token.value)
            if re.match(CLASS_CASE, class_name) is None:
                error = InvalidClassName(
                    class_name,
                    current_token.filename,
                    current_token.line,
                    current_token.column
                )
                raise ValueError(error.get_error())
            return Node('class', class_name), index + 1
        error = UnexpectedKeyword(
            'Identifier',
            str(current_token.type.name),
            current_token.filename,
            current_token.line,
            current_token.column
        )
        raise ValueError(error.get_error())

    def _parse_class_extends(self, tokens: List[Token], index: int) -> Tuple[Node|None, int]:
        token = tokens[index]
        if token.type == TokenType.EXTENDS:
            token, index = self._expected_next_token(tokens, index, TokenType.IDENTIFIER)
            if re.match(CLASS_CASE, str(token.value)) is None:
                error = InvalidClassName(
                    str(token.value),
                    token.filename,
                    token.line,
                    token.column
                )
                raise ValueError(error.get_error())
            return Node('extends', str(token.value)), index + 1
        return None, index

    def _is_token_one_of(self, tokens: List[Token], index: int, types: List[TokenType]) -> bool:
        if index < len(tokens):
            current_token = tokens[index]
            if current_token.type in types:
                return True
        return False

    def _parse_class_implements(
            self,
            tokens: List[Token],
            index: int
        ) -> Tuple[List[Node], int]:
        response: List[Node] = []
        token = tokens[index]
        if token.type != TokenType.IMPLEMENTS:
            return response, index
        if token.type == TokenType.IMPLEMENTS:
            token, index = self._expected_next_token(tokens, index, TokenType.IDENTIFIER)
            while self._is_token_one_of(tokens, index, [
                    TokenType.IDENTIFIER,
                    TokenType.COMMA
            ]):
                if token.type == TokenType.IDENTIFIER:
                    if re.match(INTERFACE_CASE, str(token.value)) is not None:
                        response.append(Node('implements', str(token.value)))
                    else:
                        error = InvalidInterfaceName(
                            str(token.value),
                            token.filename,
                            token.line,
                            token.column
                        )
                        raise ValueError(error.get_error())
                token, index = self._next_token(tokens, index)
        return response, index

    def _parse_class_attributes(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        response: List[Node] = []
        token = tokens[index]
        if token.type != TokenType.IDENTIFIER:
            return response, index
        while token.type == TokenType.IDENTIFIER and tokens[index+1].type == TokenType.COLON:
            attribute_name = str(token.value)
            if re.match(VARIABLE_CASE, attribute_name) is None:
                error = InvalidVariableName(
                    attribute_name,
                    token.filename,
                    token.line,
                    token.column
                )
                raise ValueError(error.get_error())
            token, index = self._expected_next_token(tokens, index, TokenType.COLON)
            attribute_type, index = self._expect_next_one_of_token(
                tokens,
                index,
                [
                    TokenType.CLASS_IDENTIFIER,
                    TokenType.INTERFACE_IDENTIFIER,
                    TokenType.TYPE_IDENTIFIER,
                    TokenType.ENUMERATION_IDENTIFIER,
                    TokenType.STRING_TYPE,
                    TokenType.BOOLEAN_TYPE,
                    TokenType.DECIMAL_TYPE,
                    TokenType.INTEGER_TYPE,
                    TokenType.IDENTIFIER
                ])
            attribute_node = Node('attribute', attribute_name)
            attribute_type_node = Node(str(attribute_type))
            attribute_node.add_child(attribute_type_node)
            response.append(attribute_node)
            token, index = self._next_token(tokens, index)
        return response, index

    def _parse_method_parameters(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        parameters = Node('parameters')
        token, index = self._next_token(tokens, index)
        while token.type != TokenType.RIGHT_BRACKET:
            if token.type != TokenType.IDENTIFIER:
                return response, index
            while token.type == TokenType.IDENTIFIER and tokens[index+1].type == TokenType.COLON:
                attribute_name = str(token.value)
                if re.match(VARIABLE_CASE, attribute_name) is None:
                    error = InvalidVariableName(
                        attribute_name,
                        token.filename,
                        token.line,
                        token.column
                    )
                    raise ValueError(error.get_error())
                token, index = self._expected_next_token(tokens, index, TokenType.COLON)
                attribute_type, index = self._expect_next_one_of_token(
                    tokens,
                    index,
                    [
                        TokenType.CLASS_IDENTIFIER,
                        TokenType.INTERFACE_IDENTIFIER,
                        TokenType.TYPE_IDENTIFIER,
                        TokenType.ENUMERATION_IDENTIFIER,
                        TokenType.STRING_TYPE,
                        TokenType.BOOLEAN_TYPE,
                        TokenType.DECIMAL_TYPE,
                        TokenType.INTEGER_TYPE,
                        TokenType.IDENTIFIER
                    ])
                parameter = Node('attribute', attribute_name)
                parameter_type = Node(str(attribute_type))
                parameter.add_child(parameter_type)
                parameters.add_child(parameter)
                token, index = self._next_token(tokens, index)
            if token.type == TokenType.COMMA:
                token, index = self._next_token(tokens, index)
        return parameters, index + 1

    def _parse_method_body(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        body_node = Node('body')
        token, index = self._next_token(tokens, index)
        while token.type != TokenType.RIGHT_CURLY_BRACKET:
            token, index = self._next_token(tokens, index)
        return body_node, index + 1

    def _parse_class_constructors(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        constructors: List[Node] = []
        while self._is_token_one_of(tokens, index, [
                TokenType.CONSTRUCTOR
            ]):
                constructor = Node('constructor', str(tokens[index].value))
                constructors.append(constructor)
                token, index = self._next_token(tokens, index)
                if self._expected_next_token(tokens, index, TokenType.LEFT_BRACKET):
                    parameters, index = self._parse_method_parameters(tokens, index)
                    constructor.add_child(parameters)
                    if self._expected_next_token(tokens, index, TokenType.RIGHT_BRACKET):
                        token, index = self._next_token(tokens, index)
                        if self._expected_next_token(tokens, index, TokenType.LEFT_CURLY_BRACKET):
                            body, index = self._parse_method_body(tokens, index)
                            constructor.add_child(body)
                            token, index = self._next_token(tokens, index)
                            if self._expected_next_token(
                                    tokens, index, TokenType.RIGHT_CURLY_BRACKET
                            ):
                                token, index = self._next_token(tokens, index)
        return constructors, index

    def _parse_class_methods(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        methods: List[Node] = []
        while self._is_token_one_of(tokens, index, [
                TokenType.PUBLIC,
                TokenType.PRIVATE,
                TokenType.IDENTIFIER
            ]):
            visibility_node: Node | None = None
            if tokens[index].type == TokenType.PUBLIC:
                visibility_node = Node('public')
                token, index = self._next_token(tokens, index)
            elif tokens[index].type == TokenType.PRIVATE:
                visibility_node = Node('private')
                token, index = self._next_token(tokens, index)
            if tokens[index].type == TokenType.IDENTIFIER:
                if re.match(METHOD_CASE, str(tokens[index].value)) is None:
                    error = InvalidMethodName(
                        str(tokens[index].value),
                        tokens[index].filename,
                        tokens[index].line,
                        tokens[index].column
                    )
                    raise ValueError(error.get_error())
                method = Node('method', str(tokens[index].value))
                if not visibility_node:
                    method.add_child(Node('private'))
                else:
                    method.add_child(visibility_node)
                methods.append(method)
                token, index = self._next_token(tokens, index)
                if self._expected_next_token(tokens, index, TokenType.LEFT_BRACKET):
                    parameters, index = self._parse_method_parameters(tokens, index)
                    me.add_child(parameters)
                    if self._expected_next_token(tokens, index, TokenType.RIGHT_BRACKET):
                        token, index = self._next_token(tokens, index)
                        if self._expected_next_token(tokens, index, TokenType.LEFT_CURLY_BRACKET):
                            body, index = self._parse_method_body(tokens, index)
                            method.add_child(body)
                            token, index = self._next_token(tokens, index)
                            if self._expected_next_token(
                                    tokens, index, TokenType.RIGHT_CURLY_BRACKET
                            ):
                                token, index = self._next_token(tokens, index)
        return methods, index

    def _parse_class(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        index += 1
        logging.debug('Parsing class')
        logging.debug('checking for class identifier')
        class_node, index = self._parse_class_identifier(tokens, index)
        logging.debug('checking for class extends')
        extends_node, index = self._parse_class_extends(tokens, index)
        if extends_node is not None:
            class_node.add_child(extends_node)
        logging.debug('checking for class implements')
        implements_nodes, index = self._parse_class_implements(tokens, index)
        if len(implements_nodes) > 0:
            for implements_node in implements_nodes:
                class_node.add_child(implements_node)
        logging.debug('checking for class body start "{"')
        token, index = self._expected_current_token(tokens, index, TokenType.LEFT_CURLY_BRACKET)
        logging.debug('parsing class attributes')
        attributes, index = self._parse_class_attributes(tokens, index)
        for attribute in attributes:
            class_node.add_child(attribute)
        logging.debug('parsing class constructors')
        constructors, index = self._parse_class_constructors(tokens, index)
        for constructor in constructors:
            class_node.add_child(constructor)
        logging.debug('parsing class methods')
        methods, index = self._parse_class_methods(tokens, index)
        for method in methods:
            class_node.add_child(method)
        logging.debug('checking for class body end "}"')
        token, index = self._expected_current_token(tokens, index, TokenType.RIGHT_CURLY_BRACKET)
        return class_node, index

    def _parse_import_statements(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        response: List[Node] = []
        current_token = tokens[index]
        while current_token.type == TokenType.FROM:
            node, index = self._parse_import_statement(tokens, index)
            if node is not None:
                response.append(node)
            current_token = tokens[index]
        return response, index

    def _next_token(self, tokens: List[Token], index: int) -> Tuple[Token, int]:
        index += 1
        if index >= len(tokens):
            raise ValueError('Unexpected end of file')
        return tokens[index], index

    def _current_token(self, tokens: List[Token], index: int) -> Tuple[Token, int]:
        return tokens[index], index + 1

    def _expected_next_token(
            self,
            tokens: List[Token],
            index: int,
            token_type: TokenType
        ) -> Tuple[Token, int]:
        current_token, index = self._next_token(tokens, index)
        if current_token.type != token_type:
            error = UnexpectedKeyword(
                str(token_type.value),
                str(current_token.value),
                current_token.filename,
                current_token.line,
                current_token.column
            )
            raise ValueError(error.get_error())
        return current_token, index

    def _expected_current_token(
            self,
            tokens: List[Token],
            index: int,
            token_type: TokenType
        ) -> Tuple[Token, int]:
        current_token = tokens[index]
        if current_token.type != token_type:
            if current_token.type is not TokenType.COMMENT:
                error = UnexpectedKeyword(
                    str(token_type.name),
                    str(current_token.value),
                    current_token.filename,
                    current_token.line,
                    current_token.column
                )
                raise ValueError(error.get_error())
            return self._expected_current_token(tokens, index + 1, token_type)
        return current_token, index + 1

    def _expect_next_one_of_token(
            self,
            tokens: List[Token],
            index: int,
            expected_tokens: List[TokenType]
        ) -> Tuple[Token, int]:
        current_token, index = self._next_token(tokens, index)
        if current_token.type not in expected_tokens:
            if current_token.type is not TokenType.COMMENT:
                error = UnexpectedKeyword(
                    ' or '.join([str(t.name) for t in expected_tokens]),
                    str(current_token.value),
                    current_token.filename,
                    current_token.line,
                    current_token.column
                )
                raise ValueError(error.get_error())
            current_token, index = self._next_token(tokens, index)
            return self._expect_next_one_of_token(tokens, index, expected_tokens)
        return current_token, index

    def _parse_import_statement(self, tokens: List[Token], index: int) -> Tuple[Node | None, int]:
        import_expression: str | None = None
        token, index = self._expect_next_one_of_token(
            tokens,
            index,
            [TokenType.BUILTIN, TokenType.IDENTIFIER]
        )
        if token.type == TokenType.BUILTIN:
            import_expression = str(token.type.name)
        elif token.type == TokenType.IDENTIFIER:
            import_expression = ''
            while self._is_token_one_of(tokens, index, [
                TokenType.IDENTIFIER,
                TokenType.FULL_STOP
            ]):
                if token.type == TokenType.IDENTIFIER:
                    import_expression += str(token.value)
                elif token.type == TokenType.FULL_STOP:
                    import_expression += '.'
                token, index = self._next_token(tokens, index)
            index = index - 1
        token, index = self._expected_next_token(tokens, index, TokenType.REQUIRE)
        token, index = self._expected_next_token(tokens, index, TokenType.LEFT_SQUARE_BRACKET)
        token, index = self._expected_next_token(tokens, index, TokenType.IDENTIFIER)

        if import_expression is None:
            error = InvalidImportStatement(
                token.filename,
                token.line,
                token.column
            )
            raise ValueError(error.get_error())
        if import_expression == 'BUILTIN':
            return Node('builtin'), index
        else:
            packages = import_expression.split('.')
            file_path = path(*packages)
            file_path += '.purist'
            parser = Parser(self._src_folder, self._file_reader)
            return parser.parse(file_path), index

def main(filename: str) -> None:
    """
    Entry point to the parser
    """
    parser = Parser('purist-src', FileReader())
    start = time.time()
    ast = parser.parse(filename)
    end = time.time()
    if ast is not None:
        print(ast)
    print(f'Parsed in {end - start} seconds')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python parser.py <filename>')
        print('the source code paths is currently relative to the purity-src folder')
        print('example usage: python parser.py entry.purist')
        sys.exit(1)
    logging.basicConfig(
        format='%(asctime)s [%(levelname)-8s] [%(pathname)s:%(lineno)d] %(message)s',
        level=env.get('LOGGING_LEVEL', logging.DEBUG)
    )

    main(sys.argv[1])
