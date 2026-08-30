from typing import List, Tuple

from purist.models.lexer_models import TokenType
from purist.models.node import Node
from purist.parsers.parser_handler import ParserHandler


class ServiceParser(ParserHandler):
    def parse(self, tokens: List[TokenType]) -> Tuple[Node, int]:
        return Node("", 1), 1
