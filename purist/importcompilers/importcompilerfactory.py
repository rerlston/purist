from typing import Dict

from purist.models.token import Token, TokenType
from utils.logger import Logger

class ImportCompilerFactory:
    __import_managers: Dict[TokenType, str] = {
        TokenType.BUILTIN: "purist.importcompilers.builtincompiler.BuiltInImportCompiler",
        TokenType.IDENTIFIER: "purist.importcompilers.packagecompiler.PackageImportCompiler"
    }
    __defined_managers: Dict[TokenType, object] = {}

    @staticmethod
    def get_import_compiler(token: Token) -> object | None:
        Logger.debug(token)
        if token.type in ImportCompilerFactory.__defined_managers:
            return ImportCompilerFactory.__defined_managers[token.type]
        if token.type in ImportCompilerFactory.__import_managers:
            class_name = ImportCompilerFactory.__import_managers[token.type]
            instance = ImportCompilerFactory.__get_class(class_name)()
            ImportCompilerFactory.__defined_managers[token.type] = instance
            return instance
        return None

    @staticmethod
    def __get_class(class_name: str ) -> object:
        parts = class_name.split('.')
        module = ".".join(parts[:-1])
        part = __import__( module )
        for comp in parts[1:]:
            part = getattr(part, comp)
        return part
