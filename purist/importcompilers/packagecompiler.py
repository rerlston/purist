import os

from typing import List, Tuple

from purist.importcompilers.importer import Importer
from purist.parser import Parser
from purist.models.node import Node
from purist.models.token import Token
from utils.errors import InvalidSyntaxError
from utils.filereader import FileReader
from utils.logger import Logger

class PackageImportCompiler(Importer, Parser):
    def __init__(self):
        super().__init__()
        self.__base_path = ""

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
        if source_path.endswith("."):
            error = InvalidSyntaxError(
                "Package name cannot end with a dot!",
                requester_file,
                requester_line,
                0
            )
            raise ValueError(error.get_error())
        reader = FileReader()
        file_path = source_path
        if not file_path.endswith(".purist"):
            Logger.trace(f"base path: [{self.__base_path}]")
            path_parts = file_path.split(".")
            file_path = os.path.join(self.__base_path, *path_parts)
            file_path += ".purist"
            Logger.debug(file_path)
        else:
            self.__base_path = os.path.dirname(file_path)
            Logger.debug(self.__base_path)
        content = reader.read(file_path)
        tokens = self._tokenizer.tokenize(source_path, content)

        node, index = self.parse(tokens, 0, source_path)
        return node

    def parse(
            self,
            tokens: List[Token],
            index: int,
            source_path: str|None = None
    ) -> Tuple[Node, int]:
        return self._parse_tokens(tokens, source_path), 0
