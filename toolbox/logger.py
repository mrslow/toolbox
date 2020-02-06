import os
import sys

from logging import getLogger, Formatter, FileHandler, StreamHandler


class LoggerNotFound(Exception):
    """Base Logger Exception"""


class Logger:

    def __init__(self, logdir: str, loglevel: str = 'DEBUG'):
        self.logdir = logdir
        self.loglevel = loglevel.upper()
        self.formatter = None
        self.loggers = None
        self.__post_init__()

    def __post_init__(self):
        os.makedirs(self.logdir, exist_ok=True)
        fmt = '%(asctime)s [%(levelname)s] [PID%(process)d] %(message)s'
        self.formatter = Formatter(fmt=fmt)
        self.loggers = dict()

    def __getattr__(self, item):
        return self.get(item)

    def get(self, name):
        logger = self.loggers.get(name)
        if not logger:
            raise LoggerNotFound(f'Сould not find logger named `{name}`')
        return logger

    def register(self, name: str, cout: bool = False):
        logger = getLogger(name)
        logger.setLevel(self.loglevel)
        file_handler = self._add_filehdlr(name)
        logger.addHandler(file_handler)
        if cout:
            stream_handler = self._add_streamhdlr()
            logger.addHandler(stream_handler)
        self.loggers[name] = logger

    def _add_filehdlr(self, name):
        handler = FileHandler(f'{self.logdir}/{name}.log')
        handler.setFormatter(self.formatter)
        return handler

    def _add_streamhdlr(self):
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(self.formatter)
        return handler
