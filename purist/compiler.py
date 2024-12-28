from os.path import join as path
from typing import Dict, List, Tuple

from purist.importcompilers.importcompilerfactory import ImportCompilerFactory
from purist.classparser import ClassParser
from purist.objecttypemanager import ObjectTypeManager
from purist.models.node import Node
from purist.models.token import Token, TokenType
from purist.tokenizer import Tokenizer
from utils.errors import InvalidImportStatement, NoSuchFileError
from utils.filereader import FileReader
from utils.logger import Logger

class Compiler:
    def __init__(self, file_reader: FileReader):
        self._file_reader = file_reader

        self._tokenizer = Tokenizer()
        self._root_node = None
        self._type_manager = ObjectTypeManager()
        self._parsed_files: List[str] = []
        self._parsed_file_nodes: Dict[str, Node] = {}
        self._import_parser_factory = ImportCompilerFactory()

    def compile(
            self,
            src_folder: str,
            file_path: str,
            requester_file: str|None = None,
            requester_line: int|None = None
    ) -> Node:
        """
        Parse a file and return a root Node of the AST

        Args:
            file_path: path to the file to parse
        Returns:
            Node: an abstract syntax tree root node
        """
        if file_path in self._parsed_files:
            if file_path in self._parsed_file_nodes:
                Logger.debug(f'tokenizing {file_path} from cache')
                return self._parsed_file_nodes[file_path]
            Logger.warning("cyclic dependency detected")
            return None
        full_path = path(src_folder, file_path)
        try:
            self._parsed_files.append(file_path)
            Logger.debug(f'reading {file_path}')
            Logger.info(f"Parsing: {file_path}")
            text = self._file_reader.read(full_path)
            Logger.debug(text)
            Logger.debug(f"tokenising {file_path}")
            tokens = self._tokenizer.tokenize(file_path, text)
            for token in tokens:
                Logger.debug(token)
            Logger.debug(f'parsing tokens {file_path}')
            try:
                ast = self._parse_tokens(tokens, file_path)
                self._parsed_file_nodes[file_path] = ast
                return ast
            except ValueError as e:
                Logger.debug("tokenising error")
                raise ValueError(f'Compile error: {e}') from e
        except FileNotFoundError as e:
            if (requester_file and requester_line):
                error = InvalidImportStatement(requester_file, requester_line, 0)
                raise ValueError(error.get_error()) from e
            error = NoSuchFileError(full_path, 0, 0)
            raise ValueError(error.get_error()) from e
        except RecursionError:
            Logger.error('Recursion error')
            error = InvalidImportStatement(full_path, 0, 0)
            raise ValueError(error.get_error()) from e

    def _parse_tokens(self, tokens: List[Token], filename: str) -> Node:
        token_index = 0
        if filename.endswith(".purist"):
            filename = filename[:-7]
        # filename = filename.replace('/', '.')
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

    def _parse_import_statements(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        response: List[Node] = []
        current_token = tokens[index]
        while current_token.type == TokenType.FROM:
            node, index = self._parse_import_statement(tokens, index)
            if node is not None:
                response.append(node)
            current_token = tokens[index]
        return response, index

    def _parse_import_statement(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        index += 1
        token: Token = tokens[index]
        Logger.debug(token)

        import_parser = None
        import_parser = self._import_parser_factory.get_import_parser(token, self)
        if import_parser is None:
            error = InvalidImportStatement(
                token.filename,
                token.line,
                token.column
            )
            raise ValueError(error.get_error())
        node = import_parser.parse(tokens, index)
        Logger.debug(node)
        return node, index

    def _parse_class(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        Logger.debug('parsing class tokens')
        class_parser: ClassParser = ClassParser()
        response = class_parser.parse(tokens, index)
        Logger.debug(response)
        return response
