from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from purist.models.token import Token

class Importer(ABC):
    @abstractmethod
    def tokenize(
            self,
            source_path: str,
            requester_file: str|None = None,
            requester_line: int|None = None
    ) -> List[Token]:
        """
        Compile a file and return a list of tokens

        Returns:
            Token[]: list of tokens
        """
