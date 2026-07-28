from typing import List

from purist.import_handlers.importer import Importer
from purist.tokenizer import Tokenizer

from purist.models.token import Token

from utils.filereader import FileReader

class PackageImporter(Importer):
    def __init__(self):
        self.__tokenizer = Tokenizer()

    def tokenize(self,
            source_path: str,
            requester_file: str|None = None,
            requester_line: int|None = None
    ) -> List[Token]:
        reader = FileReader()
        content = reader.read(source_path)
        return self.__tokenizer.tokenize(source_path, content)
