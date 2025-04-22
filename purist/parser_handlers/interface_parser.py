import re

from typing import List, Tuple

from purist.parser_handlers.type_parser import TypeParser
from purist.models.node import Node
from purist.models.token import Token, TokenType

from utils.logger import Logger
from utils.errors import InvalidInterfaceName

CLASS_CASE = r'^[A-Z](([a-zA-Z0-9]+)*)$'
INTERFACE_CASE = CLASS_CASE
VARIABLE_CASE = r'^[a-z]([a-zA-Z0-9])*'
CONSTANT_CASE = r'^[A-Z]([A-Z_0-9])*'

class InterfaceParser(TypeParser):
    def parse(self, tokens: List[Token], index: int) -> Node:
        index += 1
        Logger.trace('Parsing class')
        Logger.trace('checking for interface identifier')
        interface_node, index = self._parse_interface_identifier(tokens, index)
        Logger.trace("interface name found?:", interface_node is not None)
        Logger.trace('Checking for generics')
        interface_generic, index = self._parse_interface_generic(tokens, index)
        Logger.trace("generics found?:", interface_generic is not None)
        Logger.trace('checking for interface extends')
        extends_node, index = self._parse_interface_extends(tokens, index)
        if extends_node is not None:
            Logger.trace("interface extends found?: true")
            interface_node.add_child(extends_node)
        else:
            Logger.trace("interface extends found?: false")
        Logger.trace('checking for interface body start "{"')
        token, index = self._expected_current_token(tokens, index, TokenType.LEFT_CURLY_BRACKET)
        Logger.trace("interface start found?:", token.type == TokenType.LEFT_CURLY_BRACKET)
        Logger.trace('parsing interface method signatures')
        methods, index = self._parse_interface_methods(tokens, index)
        Logger.trace("interface methods found?:", len(methods.children) > 0)
        for method in methods.children:
            interface_node.add_child(method)
        Logger.trace('checking for interface body end "}"')
        Logger.debug(tokens[index])
        token, index = self._expected_current_token(tokens, index, TokenType.RIGHT_CURLY_BRACKET)
        return interface_node, index

    def _parse_interface_identifier(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        current_token = tokens[index]
        if current_token.type == TokenType.IDENTIFIER:
            interface_name = str(current_token.value)
            if re.match(INTERFACE_CASE, interface_name) is None:
                error = InvalidInterfaceName(
                    interface_name,
                    current_token.filename,
                    current_token.line,
                    current_token.column
                )
                raise ValueError(error.get_error())
            return Node('interface', interface_name), index + 1
        error = UnexpectedKeyword(
            'Identifier',
            str(current_token.type.name),
            current_token.filename,
            current_token.line,
            current_token.column
        )
        raise ValueError(error.get_error())

    def _parse_interface_generic(self, tokens: List[Token], index: int) -> Tuple[Node|None, int]:
        current_token = tokens[index]
        generic_name = None
        if current_token.type == TokenType.LEFT_ANGLE_BRACKET:
            current_token, index = self._expect_next_one_of_token(tokens, index, [TokenType.IDENTIFIER])
            generic_name = current_token.value
            current_token, index = self._expect_next_one_of_token(tokens, index, [TokenType.RIGHT_ANGLE_BRACKET])
            return Node('interface generic', str(generic_name)), index + 1
        return None, index

    def _parse_interface_extends(self, tokens: List[Token], index: int) -> Tuple[Node|None, int]:
        token = tokens[index]
        if token.type == TokenType.EXTENDS:
            token, index = self._expected_next_token(tokens, index, TokenType.IDENTIFIER)
            if re.match(INTERFACE_CASE, str(token.value)) is None:
                error = InvalidClassName(
                    str(token.value),
                    token.filename,
                    token.line,
                    token.column
                )
                raise ValueError(error.get_error())
            return Node('extends', str(token.value)), index + 1
        return None, index

    def _parse_interface_methods(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        methods = Node('methods')
        Logger.trace(tokens[index])
        token = tokens[index]
        while token.type != TokenType.RIGHT_CURLY_BRACKET:
            token, index = self._expected_current_token(tokens, index, TokenType.IDENTIFIER)
            method_name = token.value
            method = Node('methood', method_name)
            parameters, index = self._parse_method_parameters(tokens, index)
            for entry in parameters:
                parameter = Node('parameter', entry.value)
                method.add_child(parameter)
            methods.add_child(method)
            token = tokens[index]
            Logger.trace(token)
            Logger.trace(method)

        return methods, index

    def _parse_method_parameters(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        parameters = []
        token, index = self._next_token(tokens, index)
        while token.type != TokenType.RIGHT_BRACKET:
            token, index = self._next_token(tokens, index)
        return parameters, index + 1
