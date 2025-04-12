"""
Source code analysis, tokenizing and Parsing errors
"""

from abc import ABC


class Error(ABC):
    """
    Base error for all errors in the purist parser
    """
    def __init__(self, message: str, reason: str, filename: str, line: int|None = None, column: int|None = None) -> None:
        self._message = message
        self._reason = reason
        self._filename = filename
        self._line = line
        self._column = column

    def get_error(self) -> str:
        """
        Returns the error message in a preset layout for error reporting
        """
        message_padding = ' ' * len(self._message)
        error_padding = ' ' * self._column
        message = self._message
        message = f'{message}{self._reason} file: {self._filename},'
        if self._line is not None and self._column is not None:
            message = f'{message} line: {self._line}, column: {self._column}'
            message = f'{message}\r\n{message_padding}{error_padding}^'
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
    def __init__(self, line_content: str, filename: str, line: int, column: int) -> None:
        print(line_content)
        super().__init__('Unexpected character: ', line_content, filename, line, column)

class UnexpectedKeyword(Error):
    """
    Error for unexpected keywords
    """
    def __init__(self, expected: str, found: str, filename: str, line: int, column: int) -> None:
        message = f'Unexpected keyword or character: expected {expected} found: '
        super().__init__(message, found, filename, line, column)

class InvalidClassName(Error):
    """
    Error for invalid class names
    """
    def __init__(self, name: str, filename: str, line: int, column: int) -> None:
        message = f'Invalid class name: "{name}"'
        super().__init__(message, filename, line, column)

class InvalidInterfaceName(Error):
    """
    Error for invalid interface names
    """
    def __init__(self, name: str, filename: str, line: int, column: int) -> None:
        message = f'Invalid interface name: "{name}"'
        super().__init__(message, filename, line, column)

class InvalidImportStatement(Error):
    """
    Error for invalid import statements
    """
    def __init__(self, filename: str, line: int, column: int) -> None:
        message = 'Invalid import statement'
        super().__init__(message, filename, line, column)

class InvalidVariableName(Error):
    """
    Error for invalid variable names
    """
    def __init__(self, name: str, filename: str, line: int, column: int) -> None:
        message = f'Invalid variable name: "{name}"'
        super().__init__(message, filename, line, column)

class InvalidMethodName(Error):
    """
    Error for invalid method names
    """
    def __init__(self, name: str, filename: str, line: int, column: int) -> None:
        message = f'Invalid method name: "{name}"'
        super().__init__(message, filename, line, column)

class NoSuchFileError(Error):
    """
    Error for specifying a file to parse that does not exist
    """
    def __init__(self, filename: str, line: int, column: int) -> None:
        message = 'Source file not found'
        super().__init__(message, filename, None, None)

class InvalidSyntaxError(Error):
    """
    Error for syntax errors
    """
    def __init__(self, message: str, filename: str, line: int, column: int) -> None:
        super().__init__(message, filename, line, column)

class ConstantNotInitialised(Error):
    """
    Error for constants that do not have an initial value
    """
    def __init__(self, attribute_name: str, filename: str, line: int, column: int):
        message = f'Constant [{attribute_name}] not initialised'
        super().__init__(message, filename, line, column)