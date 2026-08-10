import os

from typing import List, Tuple

from purist.utils.logger import Logger
from purist.utils.errors import InvalidSyntaxError

from purist.import_handlers.import_factory import ImportFactory
from purist.parser_handlers.parser_factory import ParserFactory
from purist.models.node import Node
from purist.models.token import Token, TokenType

class Parser:
    def __init__(self):
        self.__import_factory = ImportFactory()
        self.__parser_factory = ParserFactory()

    def parse(self, source_path: str) -> Node:
        if source_path.startswith("git") or source_path.startswith("http"):
            Logger.debug("url found")
            token = Token(TokenType.URL, source_path, 0, 0, "entry")
        elif source_path.startswith("Builtin"):
            Logger.debug("Builtin found")
            token = Token(TokenType.BUILTIN, source_path, 0, 0, source_path)
        else:
            Logger.debug("package found")
            token = Token(TokenType.IDENTIFIER, source_path, 0, 0, source_path)
        importer = self.__import_factory.get_import_handler(token)
        tokens = importer.tokenize(source_path=source_path)
        Logger.trace(tokens)
        index = 0
        length = len(tokens)
        token, index = self._skip_comments(tokens, index)
        while index < length or token.type != TokenType.EOF:
            if token.type != TokenType.EOF:
                if token.type == TokenType.FROM:
                    node, index = self._parse_import_statement(tokens, index)
                    Logger.debug(node)
                else:
                    parser = self.__parser_factory.get_parser(token)
                    if parser is None:
                        error = InvalidSyntaxError(token.value, token.filename, token.line, token.column)
                        raise ValueError(error.get_error())
                    node, index = parser.parse(tokens, index)
                    token = tokens[index]
            else:
                index = index + 1
        return node

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
        import_compiler = self.__import_factory.get_import_handler(token)
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
        parser = Parser()
        node = parser.parse(path)
        Logger.debug(node)
        return node, index

    def _parse_class(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        Logger.trace('parsing class tokens')
        class_parser: ClassParser = ClassParser()
        response = class_parser.parse(tokens, index)
        Logger.debug(response)
        return response

    def _next_token(self, tokens: List[Token], index: int) -> Tuple[Token, int]:
        index += 1
        while index < len(tokens) and tokens[index].type is TokenType.COMMENT:
            index += 1
        if index >= len(tokens):
            raise ValueError('Unexpected end of file')
        return tokens[index], index

    def _skip_comments(self, tokens: List[Token], index: int) -> Tuple[Token, int]:
        token = tokens[index]
        while token.type == TokenType.COMMENT:
            token, index = self._next_token(tokens, index)
        return token, index
