import os
import sys
import time

from purist.importcompilers.importcompilerfactory import ImportCompilerFactory
from purist.models.token import Token, TokenType
from utils.logger import Logger, LogLevel

Logger.configure()

def main(filename: str) -> None:
    """
    Entry point to the parser
    """
    try:
        token = Token(TokenType.IDENTIFIER, filename, 0, 0, filename)
        compiler = ImportCompilerFactory.get_import_compiler(token)
        start = time.time()
        ast = compiler.compile(filename)
        end = time.time()

        # if ast is not None:
        Logger.info(ast)
        print(f'Parsed in {end - start} seconds')
    except ValueError as error:
        print(error)
        sys.exit(3)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python purist.py <filename>')
        print('example usage: python purist.py sample-code/entry.purist')
        sys.exit(1)

    main(sys.argv[1])
