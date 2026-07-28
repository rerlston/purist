from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from purist.classparser import ClassParser
from purist.importcompilers.importcompilerfactory import ImportCompilerFactory
from purist.objecttypemanager import ObjectTypeManager
from purist.models.node import Node
from purist.models.token import Token, TokenType
from purist.tokenizer import Tokenizer
from utils.errors import InvalidImportStatement
from utils.logger import Logger

class Importer(ABC):
    def __init__(self):
        self._tokenizer = Tokenizer()
        self._root_node = None
        self._type_manager = ObjectTypeManager()
        self._parsed_files: List[str] = []
        self._parsed_file_nodes: Dict[str, Node] = {}

    @abstractmethod
    def compile(
            self,
            source_path: str,
            requester_file: str|None = None,
            requester_line: int|None = None
    ) -> Node:
        """
        Compile a file and return a root Node of the AST

        Returns:
            Node: an abstract syntax tree root node
        """

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

        import_compiler = None
        import_compiler = ImportCompilerFactory.get_import_compiler(token)
        if import_compiler is None:
            error = InvalidImportStatement(
                token.filename,
                token.line,
                token.column
            )
            raise ValueError(error.get_error())
        path = ""
        while token.type != TokenType.REQUIRE:
            path += str(token.value)
            token, index = self._next_token(tokens, index)
        index += 1
        Logger.debug(path)
        node = import_compiler.compile(path, token.filename, token.line)
        Logger.debug(node)
        return node, index

    def _parse_class(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        Logger.trace('parsing class tokens')
        class_parser: ClassParser = ClassParser()
        response = class_parser.parse(tokens, index)
        Logger.debug(response)
        return response
