from utils.logger import Logger

from purist.import_handlers.importer import Importer
from purist.models.token import Token, TokenType

class ImportFactory:
    def __init__(self):
        self.__import_managers: Dict[TokenType, str] = {
            TokenType.BUILTIN: "purist.import_handlers.builtin_importer.BuiltInImporter",
            TokenType.IDENTIFIER: "purist.import_handlers.package_importer.PackageImporter",
            TokenType.URL: "purist.import_handlers.git_importer.GitImporter",
            TokenType.FULL_STOP: "purist.import_handlers.package_importer.PackageImporter"
        }
        self.__defined_managers: Dict[TokenType, Importer] = {}

    def get_import_handler(self, token: Token) -> Importer | None:
        Logger.debug(token)
        if token.type in self.__defined_managers:
            return self.__defined_managers[token.type]
        if token.type in self.__import_managers:
            class_name = self.__import_managers[token.type]
            Logger.debug("importer name: ", class_name)
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
