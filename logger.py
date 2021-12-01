#
# logger.py
# Written with <3 by c0repwn3r
#
# Copyright (c) 2021 c0repwn3r
import time
from colorama import init, Fore, Back, Style
init()

class LogLevel:
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4


class Logger:
    def __init__(self, name, loglevel=LogLevel.DEBUG):
        self.name = name
        self.loglevel = loglevel

    def debug(self, message):
        if self.loglevel <= LogLevel.DEBUG:
            print(f'\033[90m[{time.ctime()}] [{self.name}/DEBUG]: {message}{Style.RESET_ALL}')
        else:
            return

    def info(self, message):
        if self.loglevel <= LogLevel.INFO:
            print(f'[{time.ctime()}] [{self.name}/INFO]: {message}{Style.RESET_ALL}')
        else:
            return

    def warn(self, message):
        if self.loglevel <= LogLevel.WARN:
            print(f'{Fore.YELLOW}[{time.ctime()}] [{self.name}/WARN]: {message}{Style.RESET_ALL}')
        else:
            return

    def error(self, message):
        if self.loglevel <= LogLevel.ERROR:
            print(f'{Fore.RED}[{time.ctime()}] [{self.name}/ERROR]: {message}{Style.RESET_ALL}')
        else:
            return

    def fatal(self, message):
        if self.loglevel <= LogLevel.FATAL:
            print(f'{Fore.RED}{Style.BRIGHT}[{time.ctime()}] [{self.name}/FATAL]: {message}{Style.RESET_ALL}')
        else:
            return