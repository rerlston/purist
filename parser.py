import sys
import time

from purist_parser.parser import Parser
from utils.filereader import FileReader
from utils.logger import Logger, LogLevel

logger = Logger(log_level=LogLevel.DEBUG)

def main(filename: str) -> None:
    """
    Entry point to the parser
    """
    parser = Parser('purist-src', FileReader())
    start = time.time()
    ast = parser.parse(filename)
    end = time.time()

    if ast is not None:
        logger.debug(ast)
    logger.info(f'Parsed in {end - start} seconds')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python parser.py <filename>')
        print('the source code paths is currently relative to the purity-src folder')
        print('example usage: python parser.py entry.purist')
        sys.exit(1)

    main(sys.argv[1])
