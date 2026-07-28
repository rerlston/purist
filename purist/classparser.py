import re

from typing import List, Tuple

from purist.models.node import Node
from purist.models.token import Token, TokenType
from purist.parser import Parser
from utils.errors import (UnexpectedKeyword, InvalidClassName,
    InvalidInterfaceName, InvalidVariableName, ConstantNotInitialised)
from utils.logger import Logger

CLASS_CASE = r'^[A-Z](([a-zA-Z0-9]+)*)$'
INTERFACE_CASE = CLASS_CASE
VARIABLE_CASE = r'^[a-z]([a-zA-Z0-9])*'
CONSTANT_CASE = r'^[A-Z]([A-Z_0-9])*'

class ClassParser(Parser):
    def parse(
            self,
            tokens: List[Token],
            index: int,
            source_path: str|None = None
        ) -> Tuple[Node, int]:
        index += 1
        Logger.trace('Parsing class')
        Logger.trace('checking for class identifier')
        class_node, index = self._parse_class_identifier(tokens, index)
        Logger.trace('Checking for generics')
        class_generic, index = self._parse_class_generic(tokens, index)
        Logger.trace('checking for class extends')
        extends_node, index = self._parse_class_extends(tokens, index)
        if extends_node is not None:
            class_node.add_child(extends_node)
        Logger.trace('checking for class implements')
        implements_nodes, index = self._parse_class_implements(tokens, index)
        if len(implements_nodes) > 0:
            for implements_node in implements_nodes:
                class_node.add_child(implements_node)
        Logger.trace('checking for class body start "{"')
        token, index = self._expected_current_token(tokens, index, TokenType.LEFT_CURLY_BRACKET)
        Logger.trace('parsing class attributes')
        attributes, index = self._parse_class_attributes(tokens, index)
        for attribute in attributes:
            class_node.add_child(attribute)
        Logger.trace('parsing class constructors')
        constructors, index = self._parse_class_constructors(tokens, index)
        for constructor in constructors:
            class_node.add_child(constructor)
        Logger.trace('parsing class methods')
        methods, index = self._parse_class_methods(tokens, index)
        for method in methods:
            class_node.add_child(method)
        Logger.trace('checking for class body end "}"')
        token, index = self._expected_current_token(tokens, index, TokenType.RIGHT_CURLY_BRACKET)
        return class_node, index

    def _parse_class_identifier(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        current_token = tokens[index]
        if current_token.type == TokenType.IDENTIFIER:
            class_name = str(current_token.value)
            if re.match(CLASS_CASE, class_name) is None:
                error = InvalidClassName(
                    class_name,
                    current_token.filename,
                    current_token.line,
                    current_token.column
                )
                raise ValueError(error.get_error())
            return Node('class', class_name), index + 1
        error = UnexpectedKeyword(
            'Identifier',
            str(current_token.type.name),
            current_token.filename,
            current_token.line,
            current_token.column
        )
        raise ValueError(error.get_error())

    def _parse_class_generic(self, tokens: List[Token], index: int) -> Tuple[Node|None, int]:
        current_token = tokens[index]
        generic_name = None
        if current_token.type == TokenType.LEFT_ANGLE_BRACKET:
            current_token, index = self._expect_next_one_of_token(tokens, index, [TokenType.IDENTIFIER])
            generic_name = current_token.value
            current_token, index = self._expect_next_one_of_token(tokens, index, [TokenType.RIGHT_ANGLE_BRACKET])
            return Node('class generic', str(generic_name)), index + 1
        return None, index

    def _parse_class_extends(self, tokens: List[Token], index: int) -> Tuple[Node|None, int]:
        token = tokens[index]
        if token.type == TokenType.EXTENDS:
            token, index = self._expected_next_token(tokens, index, TokenType.IDENTIFIER)
            if re.match(CLASS_CASE, str(token.value)) is None:
                error = InvalidClassName(
                    str(token.value),
                    token.filename,
                    token.line,
                    token.column
                )
                raise ValueError(error.get_error())
            return Node('extends', str(token.value)), index + 1
        return None, index

    def _parse_class_implements(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        response: List[Node] = []
        token = tokens[index]
        if token.type != TokenType.IMPLEMENTS:
            return response, index
        if token.type == TokenType.IMPLEMENTS:
            token, index = self._expected_next_token(tokens, index, TokenType.IDENTIFIER)
            while self._is_token_one_of(tokens, index, [
                    TokenType.IDENTIFIER,
                    TokenType.COMMA
            ]):
                if token.type == TokenType.IDENTIFIER:
                    if re.match(INTERFACE_CASE, str(token.value)) is not None:
                        response.append(Node('implements', str(token.value)))
                    else:
                        error = InvalidInterfaceName(
                            str(token.value),
                            token.filename,
                            token.line,
                            token.column
                        )
                        raise ValueError(error.get_error())
                token, index = self._next_token(tokens, index)
        return response, index

    def _parse_class_attributes(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        response: List[Node] = []
        token = tokens[index]
        while self._is_token_one_of(
                tokens,
                index,
                [
                    TokenType.CLASS_IDENTIFIER,
                    TokenType.INTERFACE_IDENTIFIER,
                    TokenType.TYPE_IDENTIFIER,
                    TokenType.ENUMERATION_IDENTIFIER,
                    TokenType.STRING_TYPE,
                    TokenType.BOOLEAN_TYPE,
                    TokenType.DECIMAL_TYPE,
                    TokenType.INTEGER_TYPE,
                    TokenType.IDENTIFIER
                ]):
            token, index = self._skip_comments(tokens, index)
            attribute_type = token.value
            token, index = self._expected_next_token(tokens, index, TokenType.IDENTIFIER)
            attribute_name = str(token.value)
            Logger.debug(token)
            attribute_node = None
            initial_value = None
            if re.match(VARIABLE_CASE, attribute_name) is None:
                if re.match(CONSTANT_CASE, attribute_name) is None:
                    error = InvalidVariableName(
                        attribute_name,
                        token.filename,
                        token.line,
                        token.column
                    )
                    raise ValueError(error.get_error())
                else:
                    attribute_node = Node('constant-attribute', attribute_name)
                    next_token, index = self._next_token(tokens, index)
                    Logger.debug(next_token)
                    if not self._is_token_one_of(tokens, index, [TokenType.EQUALS]):
                        error = ConstantNotInitialised(
                            attribute_name,
                            token.filename,
                            token.line,
                            token.column
                        )
                        raise ValueError(error.get_error())
                    token, index = self._expect_next_one_of_token(tokens, index, [TokenType.INTEGER_VALUE, TokenType.STRING_VALUE])
                    initial_value = token.value

            else:
                attribute_node = Node('attribute', attribute_name)
            attribute_type_node = Node(str(attribute_type), initial_value)
            attribute_node.add_child(attribute_type_node)
            Logger.debug(attribute_node)
            response.append(attribute_node)
            token, index = self._next_token(tokens, index)

            if token.type == TokenType.EQUALS:
                token, index = self._next_token(tokens, index)
                token, index = self._next_token(tokens, index)
        return response, index

    def _parse_class_constructors(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        constructors: List[Node] = []
        while self._is_token_one_of(tokens, index, [TokenType.CONSTRUCTOR]):
            constructor = Node('constructor', str(tokens[index].value))
            Logger.trace(constructor)
            constructors.append(constructor)
            token, index = self._next_token(tokens, index)
            if self._expected_current_token(tokens, index, TokenType.LEFT_BRACKET):
                parameters, index = self._parse_method_parameters(tokens, index)
                token = tokens[index]
                constructor.add_child(parameters)
                if self._expected_next_token(tokens, index, TokenType.LEFT_CURLY_BRACKET):
                    body, index = self._parse_method_body(tokens, index)
                    constructor.add_child(body)
                    token, index = self._next_token(tokens, index)
        return constructors, index

    def _parse_class_methods(self, tokens: List[Token], index: int) -> Tuple[List[Node], int]:
        while tokens[index].type != TokenType.RIGHT_CURLY_BRACKET:
            token, index = self._next_token(tokens, index)
        return [], index

    def _parse_method_parameters(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        parameters = Node('parameters')
        token, index = self._next_token(tokens, index)
        while token.type != TokenType.RIGHT_BRACKET:
            token, index = self._next_token(tokens, index)
        return parameters, index

    def _parse_method_body(self, tokens: List[Token], index: int) -> Tuple[Node, int]:
        body_node = Node('body')
        token, index = self._next_token(tokens, index)
        while token.type != TokenType.RIGHT_CURLY_BRACKET:
            token, index = self._next_token(tokens, index)
        return body_node, index