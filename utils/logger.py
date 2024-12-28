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
    __current_log_level = os.environ if 'LOG_LEVEL' in os.environ else LogLevel.DEBUG

    @staticmethod
    def configure(log_level: LogLevel | None = None):
        if log_level is not None:
            Logger.__current_log_level = log_level
        else:
            if 'LOG_LEVEL' in os.environ:
                level = os.environ['LOG_LEVEL'].toLowerCase()
                Logger.__current_log_level = __log_level_map[level]
            else:
                Logger.__current_log_level = LogLevel.DEBUG

    @staticmethod
    def trace(*args) -> None:
        if Logger.__current_log_level == LogLevel.TRACE:
            message = Logger.__build_message(args)
            filename, lineNumber = Logger.__get_caller()
            if filename and lineNumber:
                print(Logger.__build_display(filename, int(lineNumber), message, 'TRACE', MAGENTA))
            else:
                print(Logger.__build_display('unknown', 0, message, 'TRACE', MAGENTA))

    @staticmethod
    def debug(*args) -> None:
        if Logger.__current_log_level in [LogLevel.DEBUG, LogLevel.TRACE]:
            message = Logger.__build_message(args)
            filename, lineNumber = Logger.__get_caller()
            if filename and lineNumber:
                print(Logger.__build_display(filename, int(lineNumber), message, 'DEBUG', GREEN))
            else:
                print(Logger.__build_display('unknown', 0, message, 'DEBUG', GREEN))

    @staticmethod
    def info(*args) -> None:
        if Logger.__current_log_level in [LogLevel.DEBUG, LogLevel.INFO, LogLevel.TRACE]:
            message = Logger.__build_message(args)
            filename, lineNumber = Logger.__get_caller()
            if filename is not None and lineNumber is not None:
                print(Logger.__build_display(filename, int(lineNumber), message, 'INFO ', BLUE))
            else:
                print(Logger.__build_display('unknown', 0, message, 'INFO ', BLUE))

    @staticmethod
    def warning(*args) -> None:
        if Logger.__current_log_level in [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING, LogLevel.TRACE]:
            message = Logger.__build_message(args)
            filename, lineNumber = Logger.__get_caller()
            if filename is not None and lineNumber is not None:
                print(Logger.__build_display(filename, int(lineNumber), message, 'WARN ', ORANGE))
            else:
                print(Logger.__build_display('unknown', 0, message, 'WARN', ORANGE))

    @staticmethod
    def error(*args) -> None:
        message = Logger.__build_message(args)
        filename, lineNumber = Logger.__get_caller()
        stack = Logger.__get_stack()[2:]
        if filename is not None and lineNumber is not None:
            print(Logger.__build_display(filename, int(lineNumber), message, 'ERROR', RED, stack))
        else:
            print(Logger.__build_display('unknown', 0, message, 'ERROR', RED, stack))

    @staticmethod
    def error_no_stack(*args) -> None:
        message = Logger.__build_message(args)
        filename, lineNumber = Logger.__get_caller()
        if filename is not None and lineNumber is not None:
            print(Logger.__build_display(filename, int(lineNumber), message, 'ERROR', RED))
        else:
            print(Logger.__build_display('unknown', 0, message, 'ERROR', RED))

    @staticmethod
    def __build_message(*args):
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

    @staticmethod
    def __space_pad(value: str, length: int) -> str:
        response = value
        while len(response) < length:
            response += ' '
        return response

    @staticmethod
    def __zero_pad(value: int, length: int) -> str:
        response = str(value)
        while len(response) < length:
            response = '0' + response
        return response

    @staticmethod
    def __zero_pad_right(value: int, length: int) -> str:
        response = str(value)
        while len(response) < length:
            response = response + '0'
        return response

    @staticmethod
    def __format_date_time(date_time: datetime, date_format: str|None = None) -> str:
        year = date_time.year
        month = Logger.__zero_pad(date_time.month, 2)
        day = Logger.__zero_pad(date_time.day, 2)
        hour = Logger.__zero_pad(date_time.hour, 2)
        minute = Logger.__zero_pad(date_time.minute, 2)
        seconds = Logger.__zero_pad(date_time.second, 2)
        milliseconds = Logger.__zero_pad_right(str(date_time.microsecond), 6).replace(r"/ /g", "0")

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

    @staticmethod
    def __build_standard_display(
            filename: str,
            line_number: int,
            date_time: str,
            message: str,
            log_level: str,
            colour: str,
            stack: list[dict[str, str]]|None = None) -> str:
        log_level_resized = Logger.__space_pad(log_level, 5)
        if stack:
            stack_display = ''
            for entry in stack:
                stack_display += f'\t{RESET}at {colour}{entry["filename"]}:{entry["lineNumber"]}\n'
            return f'[{colour}{log_level_resized}{RESET}][{date_time}] {colour}{message}\n{stack_display}{RESET}'
        else:
            return f'[{colour}{log_level_resized}{RESET}][{date_time}][{filename}:{line_number}] {colour}{message}{RESET}'

    @staticmethod
    def __build_display(
            filename: str,
            line_number: int,
            message: str,
            log_level: str,
            colour: str,
            stack: list[dict[str, str]]|None = None) -> str:
        date_time = Logger.__format_date_time(datetime.now())
        return Logger.__build_standard_display(
            filename, line_number, date_time, message,
            log_level, colour, stack
        )

    @staticmethod
    def __get_caller() -> tuple[str, str]:
        stack = Logger.__get_stack()
        caller_info = stack[3]
        path = Logger.__find_match(caller_info['filename'], os.getcwd())
        filename = caller_info['filename']
        filename = filename[len(path) + 1:]
        line_number = caller_info['lineNumber']
        return filename, line_number

    @staticmethod
    def __find_match(filepath: str, current_path: str) -> str:
        i = 0
        char_left = filepath[i]
        char_right = current_path[i]
        while i < len(current_path) and char_left == char_right:
            i = i + 1
            if i != len(current_path):
                char_left = filepath[i]
                char_right = current_path[i]
        return current_path[0: i]

    @staticmethod
    def __get_stack() -> list[dict[str, str]]:
        stack_list = []
        frame_info = inspect.stack()
        for frame in frame_info:
            if '/loggers.py' not in frame.filename:
                stack_list.append({
                    'filename': frame.filename,
                    'lineNumber': frame.lineno
                })
        return stack_list
