from typing import List, Protocol, Tuple

from purist.models.lexer_models import TokenType
from purist.models.node import Node


class ParserHandler(Protocol):
    def parse(self, tokens: List[TokenType]) -> Tuple[Node, int]: ...
