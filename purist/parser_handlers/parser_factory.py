from purist.models.token import Token, TokenType
from purist.parser_handlers.type_parser import TypeParser
from utils.logger import Logger

class ParserFactory:
    def __init__(self):
        self.__parsers: Dict[TokenType, str] = {
            TokenType.CLASS: "purist.parser_handlers.class_parser.ClassParser",
            TokenType.INTERFACE: "purist.parser_handlers.interface_parser.InterfaceParser",
            # TokenType.DATA_TYPE: "purist.parser_handlers.data_type_parser.DataTypeParser"
        }
        self.__defined_managers: Dict[TokenType, TypeParser] = {}

    def get_parser(self, token: Token) -> TypeParser | None:
        Logger.debug(token)
        if token.type in self.__defined_managers:
            return self.__defined_managers[token.type]
        if token.type in self.__parsers:
            class_name = self.__parsers[token.type]
            Logger.debug("parser name: ", class_name)
            instance = self.__get_class(class_name)()
            self.__defined_managers[token.type] = instance
            return instance
        return None

    def __get_class(self, class_name: str ) -> object:
        parts = class_name.split('.')
        module = ".".join(parts[:-1])
        part = __import__( module )
        for comp in parts[1:]:
            part = getattr(part, comp)
        return part
