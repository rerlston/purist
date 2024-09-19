"""
Purist source code lexer, reads source code and discovers words, numbers, operators, etc
"""

from typing import Tuple

from errors import DecodeError, Error

VALID_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890'


class Lexer():
    """
    Purist Lexer, reads source code and discovers words, numbers, operators, etc
    """

    def __init__(self, filepath: str, text: str) -> None:
        self._filepath = filepath
        self._text = text
        self._line = 0
        self._column = 0
        self._lines = text.splitlines()

    def next(self) -> Tuple[str | None, Error | None, int, int]:
        """
        Reads the next source code value from the file
        Returns a tuple of a discovered value and a specific error if encountered

        Returns:
            Tuple[str|None, Error|None]: (discovered value, error)
        """
        response: str | None = None
        error: Error | None = None
        start_column: int = self._column
        start_line: int = self._line
        while response is None and error is None and self._line < len(self._lines):
            while response is None and error is None and self._column < len(
                self._lines[self._line]
            ):
                start_column = self._column
                character: str = self._lines[self._line][self._column]
                while character == ' ' or character == '\t':
                    self._column += 1
                    character = self._lines[self._line][self._column]
                if character.isalpha():
                    response, error = self._fetch_word()
                elif character.isdigit() or character == '-':
                    response, error = self._fetch_number()
                elif character == '"':
                    response, error = self._fetch_string()
                elif character == '/':
                    response, error = self._fetch_comment_or_divide()
                elif character in [
                    '[', ']', '{', '}', '(', ')', ',',
                    ':', '=', '<', '>', '.', '!', '|'
                ]:
                    self._column += 1
                    response = character
                else:
                    error = DecodeError(
                        character,
                        self._filepath,
                        self._line,
                        self._column
                    )
            if response is None or error is None:
                if self._column >= len(self._lines[self._line]):
                    self._line += 1
                    self._column = 0
        return response, error, start_line + 1, start_column + 1

    def _fetch_word(self) -> Tuple[str | None, Error | None]:
        word = ''
        character = self._lines[self._line][self._column]
        while character in VALID_CHARACTERS and self._column < len(self._lines[self._line]):
            word += character
            self._column += 1
            if self._column < len(self._lines[self._line]):
                character = self._lines[self._line][self._column]
        return word, None

    def _fetch_number(self) -> Tuple[str | None, Error | None]:
        number = ''
        character = self._lines[self._line][self._column]
        while character in '-1234567890.' and self._column < len(self._lines[self._line]):
            if character == '.':
                if '.' in number:
                    return None, DecodeError(
                        'too many decimal points',
                        self._filepath,
                        self._line,
                        self._column
                    )
            number += character
            self._column += 1
            if self._column < len(self._lines[self._line]):
                character = self._lines[self._line][self._column]
        return number, None

    def _fetch_string(self) -> Tuple[str | None, Error | None]:
        string = ''
        self._column += 1
        character = self._lines[self._line][self._column]
        while character != '"' and self._line < len(self._lines):
            string += character
            self._column += 1
            if self._column >= len(self._lines[self._line]):
                self._line += 1
                self._column = 0
                string += '\n'
            character = self._lines[self._line][self._column]
            if character == '"' and string[-1] == '\\':
                string += '"'
                self._column += 1
                character = self._lines[self._line][self._column]
        self._column += 1
        return f'"{string}"', None

    def _fetch_comment_or_divide(self) -> Tuple[str | None, Error | None]:
        first_character = self._lines[self._line][self._column]
        if self._column + 1 < len(self._lines[self._line]):
            if first_character == '/' and self._lines[self._line][self._column + 1] == '/':
                comment = self._lines[self._line][self._column:]
                self._column = len(self._lines[self._line])
                return comment, None
            self._column += 1
            return '/', None
        return None, DecodeError(first_character, self._filepath, self._line, self._column)
