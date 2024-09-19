"""
Purist Parser, entry point to parse the purist source code
"""
import json
import re
import sys

from os.path import join as path

import time
from typing import Any, Dict, List, Tuple
from errors import InvalidClassName, InvalidImportStatement, InvalidInterfaceName, UnexpectedKeyword
from tokenizer import Token, TokenType, Tokenizer

PASCAL_CASE = r'^[A-Z](([a-zA-Z0-9]+[A-Z]?)*)$'
CLASS_CASE = PASCAL_CASE
INTERFACE_CASE = PASCAL_CASE
CAMEL_CASE = r'^[a-z]|[A-Z0-9])[a-z]*'
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


class Parser():
    """
    Purist Parser, once it has tokens it checks if the tokens can form a valid AST
    """

    def __init__(self, src_folder: str) -> None:
        self._tokenizer = Tokenizer()
        self._src_folder = src_folder
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
            with open(full_path, 'r') as file:
                self._parsed_files.append(file_path)
                text = file.read()
                tokens = self._tokenizer.tokenize(file_path, text)
                try:
                    ast = self._parse_tokens(tokens, file_path)
                    self._parsed_file_nodes[file_path] = ast
                    return ast
                except ValueError as e:
                    print(f'Compile errors: {e}')
                    sys.exit(1)
        except FileNotFoundError:
            print(f'File not found: {full_path}')
            sys.exit(1)
        except RecursionError:
            print('Recursion error')
            sys.exit(1)

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
        class_node: Node | None = None
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
            class_node = Node('class', class_name)
            index += 1
        else:
            error = UnexpectedKeyword(
                'Identifier',
                str(current_token.type.name),
                current_token.filename,
                current_token.line,
                current_token.column
            )
            raise ValueError(error.get_error())
        return class_node, index

    def _parse_class_extends(self, tokens: List[Token], index: int) -> Tuple[Node|None, int]:
        token, index = self._next_token(tokens, index)
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
            return Node('extends', str(token.value)), index
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
        token, index = self._next_token(tokens, index)
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

    def _parse_class(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        index += 1
        class_node, index = self._parse_class_identifier(tokens, index)
        extends_node, index = self._parse_class_extends(tokens, index)
        if extends_node is not None:
            class_node.add_child(extends_node)
        implements_nodes, index = self._parse_class_implements(tokens, index)
        if len(implements_nodes) > 0:
            for implements_node in implements_nodes:
                class_node.add_child(implements_node)
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

    def _expected_next_token(
            self,
            tokens: List[Token],
            index: int,
            token_type: TokenType
        ) -> Tuple[Token, int]:
        current_token, index = self._next_token(tokens, index)
        if current_token.type != token_type:
            error = UnexpectedKeyword(
                str(token_type.name),
                str(current_token.type.name),
                current_token.filename,
                current_token.line,
                current_token.column
            )
            raise ValueError(error.get_error())
        return current_token, index

    def _expect_next_one_of_token(
            self,
            tokens: List[Token],
            index: int,
            expected_tokens: List[TokenType]
        ) -> Tuple[Token, int]:
        current_token, index = self._next_token(tokens, index)
        if current_token.type not in expected_tokens:
            error = UnexpectedKeyword(
                ' or '.join([str(t.name) for t in expected_tokens]),
                str(current_token.type.name),
                current_token.filename,
                current_token.line,
                current_token.column
            )
            raise ValueError(error.get_error())
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
            return self.parse(file_path), index

def main(filename: str) -> None:
    """
    Entry point to the parser
    """
    parser = Parser('purist-src')
    start = time.time()
    ast = parser.parse(filename)
    end = time.time()
    print(ast)
    print(f'Parsed in {end - start} seconds')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python parser.py <filename>')
        print('the source code paths is currently relative to the purity-src folder')
        print('example usage: python parser.py entry.purist')
        sys.exit(1)
    main(sys.argv[1])
