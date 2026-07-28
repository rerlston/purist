import os
import sys
import time

from purist.parser import Parser
from purist.models.token import Token, TokenType
from utils.logger import Logger, LogLevel

Logger.configure()

def main(source_path: str) -> None:
    """
    Entry point to the parser
    """
    try:
        start = time.time()
        
        parser = Parser()
        ast = parser.parse(source_path)
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
