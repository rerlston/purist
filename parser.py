"""
Purist Parser, entry point to parse the purist source code
"""
import json
import sys

from os.path import join as path

from typing import Any, Dict, List, Tuple
from errors import UnexpectedKeyword
from tokenizer import Token, TokenType, Tokenizer

class Node():
    """
    Abstract Syntax Tree Node
    """
    def __init__(self, node_name: str, value: str|int|float|None = None) -> None:
        self._node_name = node_name
        self._value = value
        self._children: 'List[Node]|None' = None

    @property
    def children(self) -> 'List[Node]|None':
        return self._children

    def add_child(self, node: 'Node|None') -> None:
        if node is not None:
            if self._children is None:
                self._children = []
            self._children.append(node)

    @property
    def value(self) -> str|int|float|None:
        return self._value

    @value.setter
    def value(self, value: str|int|float) -> None:
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

    def parse(self, file_path: str) -> Node|None:
        """
        Parse a file and return a root Node of the AST

        Args:
            file_path: path to the file to parse
        Returns:
            Node: an abstract syntax tree root node
        """
        if file_path in self._parsed_files:
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

    def _parse_class(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        index += 1
        class_name: str|None = None
        current_token = tokens[index]
        class_node: Node | None = None
        if current_token.type == TokenType.IDENTIFIER:
            class_name = str(current_token.value)
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
        if index < len(tokens):
            current_token = tokens[index]
            if current_token.type == TokenType.EXTENDS:
                index += 1
                if index < len(tokens):
                    current_token = tokens[index]
                    if current_token.type == TokenType.IDENTIFIER:
                        class_node.add_child(Node('extends', str(current_token.value)))
                        index += 1
                    else:
                        error = UnexpectedKeyword(
                            'Class Identifier',
                            str(current_token.type.name),
                            current_token.filename,
                            current_token.line,
                            current_token.column
                        )
                        raise ValueError(error.get_error())
                if index < len(tokens):
                    current_token = tokens[index]
            if index < len(tokens):
                current_token = tokens[index]
                if current_token.type == TokenType.IMPLEMENTS:
                    index += 1
                    if index < len(tokens):
                        current_token = tokens[index]
                        if current_token.type == TokenType.IDENTIFIER:
                            while current_token.type == TokenType.IDENTIFIER or current_token.type == TokenType.COMMA:
                                if current_token.type == TokenType.IDENTIFIER:
                                    class_node.add_child(Node('implements', str(current_token.value)))
                                index += 1
                                current_token = tokens[index]
                        else:
                            error = UnexpectedKeyword(
                                'Class Identifier',
                                str(current_token.type.name),
                                current_token.filename,
                                current_token.line,
                                current_token.column
                            )
                            raise ValueError(error.get_error())
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

    def _parse_import_statement(self, tokens: List[Token], index: int) -> Tuple[Node|None, int]:
        current_token = tokens[index]
        index += 1
        import_expression: str|None = None
        if index < len(tokens):
            current_token = tokens[index]
            if current_token.type == TokenType.BUILTIN:
                import_expression = str(current_token.type.name)
                index += 1
            elif current_token.type == TokenType.IDENTIFIER:
                import_expression = ''
                while current_token.type == TokenType.IDENTIFIER or current_token.type == TokenType.FULL_STOP:
                    if current_token.type == TokenType.IDENTIFIER:
                        import_expression += str(current_token.value)
                    if current_token.type == TokenType.FULL_STOP:
                        import_expression += '.'
                    index += 1
                    if index < len(tokens):
                        current_token = tokens[index]
            else:
                value = str(current_token.type.name)
                if current_token.value is not None:
                    value = str(current_token.value)
                error = UnexpectedKeyword(
                    'Builtin or identifier',
                    value,
                    current_token.filename,
                    current_token.line,
                    current_token.column
                )
                raise ValueError(error.get_error())
            if index < len(tokens):
                current_token = tokens[index]
                if current_token.type == TokenType.REQUIRE:
                    index += 1
                else:
                    error = UnexpectedKeyword(
                        'require',
                        str(current_token.value),
                        current_token.filename,
                        current_token.line,
                        current_token.column
                    )
                    raise ValueError(error.get_error())
                if index < len(tokens):
                    current_token = tokens[index]
                    if current_token.type == TokenType.LEFT_SQUARE_BRACKET:
                        index += 1
                    else:
                        error = UnexpectedKeyword(
                            '[',
                            str(current_token.value),
                            current_token.filename,
                            current_token.line,
                            current_token.column
                        )
                        raise ValueError(error.get_error())
                    if index < len(tokens):
                        current_token = tokens[index]
                        if current_token.type == TokenType.IDENTIFIER:
                            index += 1
                        else:
                            error = UnexpectedKeyword(
                                'class or interface name',
                                str(current_token.value),
                                current_token.filename,
                                current_token.line,
                                current_token.column
                            )
                            raise ValueError(error.get_error())
                    else:
                        raise ValueError('Unexpected end of file')
                else:
                    raise ValueError('Unexpected end of file')
            else:
                raise ValueError('Unexpected end of file')
        else:
            raise ValueError('Unexpected end of file')

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
    ast = parser.parse(filename)
    print(ast)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python parser.py <filename>')
        print('the source code paths is currently relative to the purity-src folder')
        print('example usage: python parser.py entry.purist')
        sys.exit(1)
    main(sys.argv[1])
