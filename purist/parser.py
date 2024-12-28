from typing import List, Tuple

from abc import ABC, abstractmethod

from purist.models.node import Node
from purist.models.token import Token, TokenType
from utils.errors import UnexpectedKeyword
from utils.logger import Logger


class Parser(ABC):
    @abstractmethod
    def parse(
            self,
            tokens: List[Token],
            index: int,
            source_path: str|None = None
    ) -> Tuple[Node, int]:
        pass

    def _parse_tokens(self, tokens: List[Token], filename: str) -> Node:
        Logger.debug(tokens)
        token_index = 0
        if filename.endswith(".purist"):
            filename = filename[:-7]
        # filename = filename.replace('/', '.')
        root_node: Node = Node('source', filename)
        while token_index < len(tokens):
            token = tokens[token_index]
            if token.type == TokenType.FROM:
                nodes, token_index = self._parse_import_statements(tokens, token_index)
                for node in nodes:
                    root_node.add_child(node)
            elif token.type == TokenType.CLASS:
                node, token_index = self._parse_class(tokens, token_index)
                root_node.add_child(node)
            else:
                token_index += 1
        return root_node

    def _expect_next_one_of_token(
            self,
            tokens: List[Token],
            index: int,
            expected_tokens: List[TokenType]
        ) -> Tuple[Token, int]:
        current_token, index = self._next_token(tokens, index)
        if current_token.type not in expected_tokens:
            if current_token.type is not TokenType.COMMENT:
                error = UnexpectedKeyword(
                    ' or '.join([str(t.name) for t in expected_tokens]),
                    str(current_token.value),
                    current_token.filename,
                    current_token.line,
                    current_token.column
                )
                raise ValueError(error.get_error())
            current_token, index = self._next_token(tokens, index)
            return self._expect_next_one_of_token(tokens, index, expected_tokens)
        return current_token, index

    def _next_token(self, tokens: List[Token], index: int) -> Tuple[Token, int]:
        index += 1
        while index < len(tokens) and tokens[index].type is TokenType.COMMENT:
            index += 1
        if index >= len(tokens):
            raise ValueError('Unexpected end of file')
        return tokens[index], index

    def _is_token_one_of(self, tokens: List[Token], index: int, types: List[TokenType]) -> bool:
        if index < len(tokens):
            current_token = tokens[index]
            if current_token.type in types:
                return True
        return False

    def _expected_next_token(
            self,
            tokens: List[Token],
            index: int,
            token_type: TokenType
        ) -> Tuple[Token, int]:
        current_token, index = self._next_token(tokens, index)
        if current_token.type != token_type:
            error = UnexpectedKeyword(
                str(token_type.value),
                str(current_token.value),
                current_token.filename,
                current_token.line,
                current_token.column
            )
            raise ValueError(error.get_error())
        return current_token, index

    def _expected_current_token(
            self,
            tokens: List[Token],
            index: int,
            token_type: TokenType
        ) -> Tuple[Token, int]:
        current_token = tokens[index]
        if current_token.type != token_type:
            if current_token.type is not TokenType.COMMENT:
                error = UnexpectedKeyword(
                    str(token_type.name),
                    str(current_token.value),
                    current_token.filename,
                    current_token.line,
                    current_token.column
                )
                raise ValueError(error.get_error())
            return self._expected_current_token(tokens, index + 1, token_type)
        return current_token, index + 1

    def _skip_comments(self, tokens: List[Token], index: int) -> Tuple[Token, int]:
        token = tokens[index]
        while token.type == TokenType.COMMENT:
            token, index = self._next_token(tokens, index)
        return token, index
