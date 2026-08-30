from typing import List, Tuple, override

from purist.models.lexer_models import LexerType
from purist.models.node import Node
from purist.parsers.parser_handler import ParserHandler

class ImportParser(ParserHandler):
    @override
    def parse(self, tokens: List[LexerType]) -> Tuple[Node, int]
        