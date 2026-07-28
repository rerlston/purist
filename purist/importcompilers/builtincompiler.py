import os

from typing import List, Tuple

from purist.importcompilers.importer import Importer
from purist.parser import Parser
from purist.models.node import Node
from purist.models.token import Token
from utils.errors import InvalidSyntaxError
from utils.filereader import FileReader

class BuiltInImportCompiler(Importer, Parser):
    def compile(
            self,
            source_path: str,
            requester_file: str|None = None,
            requester_line: int|None = None
    ) -> Node:
        if source_path.endswith("."):
            error = InvalidSyntaxError(
                "Package name cannot end with a dot!",
                requester_file,
                requester_line,
                0
            )
            raise ValueError(error.get_error())
        file_path = source_path.replace("Builtin", "purist-src")
        path_parts = file_path.split(".")
        file_path = os.path.join(*path_parts)
        file_path += '.purist'

        reader = FileReader()
        content = reader.read(file_path)
        tokens = self._tokenizer.tokenize(source_path, content)

        return self.parse(tokens, 0, source_path)

    def parse(
            self,
            tokens: List[Token],
            index: int,
            source_path: str|None = None
    ) -> Tuple[Node, int]:
        return self._parse_tokens(tokens, source_path)
