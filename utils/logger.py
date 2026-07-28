import inspect
import os

from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

__log_level_map = {
    'trace': LogLevel.TRACE,
    'debug': LogLevel.DEBUG,
    'info': LogLevel.INFO,
    'warn': LogLevel.WARNING,
    'error': LogLevel.ERROR
}

GREEN = "\x1b[32m"
BLUE = "\x1b[34m"
ORANGE = "\x1b[33m"
MAGENTA = "\x1b[35m"
RED = "\x1b[31m"
RESET = "\x1b[0m"

class Logger:
    _log_level: LogLevel

    def __init__(
            self,
            log_level: LogLevel|None = None
    ) -> None:
        if log_level is not None:
            self._log_level = log_level
        else:
            if 'LOG_LEVEL' in os.environ:
                level = os.environ['LOG_LEVEL'].toLowerCase()
                self._log_level = __log_level_map[level]
            else:
                self._log_level = LogLevel.DEBUG

    def trace(self, *args) -> None:
        if self._log_level == LogLevel.DEBUG:
            message = self.__build_message(args)
            filename, lineNumber = self.__get_caller()
            if filename and lineNumber:
                print(self.__build_display(filename, int(lineNumber), message, 'TRACE', MAGENTA))
            else:
                print(self.__build_display('unknown', 0, message, 'TRACE', MAGENTA))

    def debug(self, *args) -> None:
        if self._log_level == LogLevel.DEBUG:
            message = self.__build_message(args)
            filename, lineNumber = self.__get_caller()
            if filename and lineNumber:
                print(self.__build_display(filename, int(lineNumber), message, 'DEBUG', GREEN))
            else:
                print(self.__build_display('unknown', 0, message, 'DEBUG', GREEN))

    def info(self, *args) -> None:
        if self._log_level == LogLevel.DEBUG or self._log_level == LogLevel.INFO:
            message = self.__build_message(args)
            filename, lineNumber = self.__get_caller()
            if filename is not None and lineNumber is not None:
                print(self.__build_display(filename, int(lineNumber), message, 'INFO ', BLUE))
            else:
                print(self.__build_display('unknown', 0, message, 'INFO ', BLUE))

    def warning(self, *args) -> None:
        if self._log_level == LogLevel.DEBUG or self._log_level == LogLevel.INFO or self._log_level == LogLevel.WARNING:
            message = self.__build_message(args)
            filename, lineNumber = self.__get_caller()
            if filename is not None and lineNumber is not None:
                print(self.__build_display(filename, int(lineNumber), message, 'WARN', ORANGE))
            else:
                print(self.__build_display('unknown', 0, message, 'WARN', ORANGE))

    def error(self, *args) -> None:
        message = self.__build_message(args)
        filename, lineNumber = self.__get_caller()
        stack = self.__get_stack()
        if filename is not None and lineNumber is not None:
            print(self.__build_display(filename, int(lineNumber), message, 'ERROR', RED, stack))
        else:
            print(self.__build_display('unknown', 0, message, 'ERROR', RED, stack))
            
    def error_no_stack(self, *args) -> None:
        message = self.__build_message(args)
        filename, lineNumber = self.__get_caller()
        if filename is not None and lineNumber is not None:
            print(self.__build_display(filename, int(lineNumber), message, 'ERROR', RED))
        else:
            print(self.__build_display('unknown', 0, message, 'ERROR', RED))

    def __build_message(self, *args):
        response = ''
        items = []
        for arg in args:
            if isinstance(arg, tuple):
                for item in arg:
                    items.append(str(item))
            else:
                items.append(str(arg))
        response = " ".join(items)
        return response

    def __space_pad(self, value: str, length: int) -> str:
        response = value
        while len(response) < length:
            response += ' '
        return response

    def __zero_pad(self, value: int, length: int) -> str:
        response = str(value)
        while len(response) < length:
            response = '0' + response
        return response

    def __zero_pad_right(self, value: int, length: int) -> str:
        response = str(value)
        while len(response) < length:
            response = response + '0'
        return response

    def __format_date_time(self, date_time: datetime, date_format: str|None = None) -> str:
        year = date_time.year
        month = self.__zero_pad(date_time.month, 2)
        day = self.__zero_pad(date_time.day, 2)
        hour = self.__zero_pad(date_time.hour, 2)
        minute = self.__zero_pad(date_time.minute, 2)
        seconds = self.__zero_pad(date_time.second, 2)
        milliseconds = self.__zero_pad_right(str(date_time.microsecond), 6).replace(r"/ /g", "0")

        if date_format is None:
            return f'{year}-{month}-{day} {hour}:{minute}:{seconds}.{milliseconds}'
        response = date_format
        response = response.replace('yyyy', str(year))
        response = response.replace('MM', month)
        response = response.replace('dd', day)
        response = response.replace('hh', hour)
        response = response.replace('mm', minute)
        response = response.replace('ss', seconds)
        response = response.replace('SSS', milliseconds)

        return response

    def __build_standard_display(
            self,
            filename: str,
            line_number: int,
            date_time: str,
            message: str,
            log_level: str,
            colour: str,
            stack: list[dict[str, str]]|None = None) -> str:
        log_level_resized = self.__space_pad(log_level, 5)
        if stack:
            stack_display = ''
            for entry in stack:
                stack_display += f'\t{RESET}at {colour}{entry["filename"]}:{entry["lineNumber"]}\n'
            return f'[{colour}{log_level_resized}{RESET}][{date_time}] {colour}{message}\n{stack_display}{RESET}'
        else:
            return f'[{colour}{log_level_resized}{RESET}][{date_time}][{filename}:{line_number}] {colour}{message}{RESET}'

    def __build_display(
            self,
            filename: str,
            line_number: int,
            message: str,
            log_level: str,
            colour: str,
            stack: list[dict[str, str]]|None = None) -> str:
        date_time = self.__format_date_time(datetime.now())
        return self.__build_standard_display(
            filename, line_number, date_time, message,
            log_level, colour, stack
        )

    def __get_caller(self) -> tuple[str, str]:
        stack = self.__get_stack()
        caller_info = stack[0]
        path = self.__find_match(caller_info['filename'], os.getcwd())
        filename = caller_info['filename']
        filename = filename[len(path) + 1:]
        line_number = caller_info['lineNumber']
        return filename, line_number

    def __find_match(self, filepath: str, current_path: str) -> str:
        i = 0
        char_left = filepath[i]
        char_right = current_path[i]
        while i < len(current_path) and char_left == char_right:
            i = i + 1
            if i != len(current_path):
                char_left = filepath[i]
                char_right = current_path[i]
        return current_path[0: i]

    def __get_stack(self) -> list[dict[str, str]]:
        stack_list = []
        frame_info = inspect.stack()
        for frame in frame_info:
            if '/loggers.py' not in frame.filename:
                stack_list.append({
                    'filename': frame.filename,
                    'lineNumber': frame.lineno
                })
        return stack_list
