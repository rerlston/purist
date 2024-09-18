"""
Source code analysis, tokenizing and Parsing errors
"""

from abc import ABC


class Error(ABC):
    """
    Base error for all errors in the purist parser
    """
    def __init__(self, message: str, filename: str, line: int, column: int) -> None:
        self._message = message
        self._filename = filename
        self._line = line
        self._column = column

    def get_error(self) -> str:
        """
        Returns the error message in a preset layout for error reporting
        """
        message = self._message
        message = f'{message} file: {self._filename},'
        message = f'{message} line: {self._line + 1}, column: {self._column + 1}'
        return message

class InvalidComment(Error):
    """
    Error for invalid comments
    """
    def __init__(self, filename: str, line: int, column: int) -> None:
        super().__init__('Invalid Comment', filename, line, column)

class DecodeError(Error):
    """
    Error for decoding errors
    """
    def __init__(self, character: str, filename: str, line: int, column: int) -> None:
        super().__init__(f'Unexpected character: "{character}"', filename, line, column)

class UnexpectedKeyword(Error):
    """
    Error for unexpected keywords
    """
    def __init__(self, expected: str, found: str, filename: str, line: int, column: int) -> None:
        message = f'Unexpected keyword: "{found}" expected "{expected}"'
        super().__init__(message, filename, line, column)
