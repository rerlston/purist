import os

from typing import List

from purist.import_handlers.importer import Importer
from purist.tokenizer import Tokenizer
from purist.models.token import Token
from utils.filereader import FileReader

class BuiltInImporter(Importer):
    def __init__(self):
        self.__tokenizer = Tokenizer()

    def tokenize(self, source_path:str) -> List[Token]:
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
        return self.__tokenizer.tokenize(source_path, content)
