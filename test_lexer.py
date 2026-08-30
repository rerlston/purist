import sys
import time

from purist.lexer.lexer import Lexer
from purist.models.lexer_models import LexerResult, LexerState, LexerType
from purist.utils.filereader import FileReader
from purist.utils.errors import Error
from purist.utils.logger import Logger

Logger.configure()


def main(source_path: str) -> None:
    """
    Entry point to the lexer tester
    """
    try:
        start = time.time()
        file_reader = FileReader()
        content = file_reader.read(source_path)
        Logger.info(content)

        state = LexerState(filepath="test", text=content)
        lexer = Lexer(Lexer.setup(), state)
        tokens = []
        response: LexerResult | Error = lexer.next()
        while isinstance(response, LexerResult) and response.type is not LexerType.EOF:
            tokens.append(response)
            response = lexer.next()
            # Logger.info(response)
        end = time.time()
        if isinstance(response, Error):
            Logger.error(response)
        else:
            for token in tokens:
                Logger.info(token)
        print(f"Parsed in {end - start} seconds")
    except ValueError as error:
        print(error)
        sys.exit(3)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python purist.py <filename>")
        print("example usage: python purist.py sample-code/entry.purist")
        sys.exit(1)

    main(sys.argv[1])
