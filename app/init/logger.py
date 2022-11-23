import os
import logging
from logging.handlers import RotatingFileHandler

from typing import List


class LoggBase():
    def __init__(
        self,
        level=logging.DEBUG,
        format="%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    ) -> None:
        self.level = level
        self.format = format
        self.datefmt = datefmt
        logging.getLogger().setLevel(self.level)


class LoggerInitializer(LoggBase):
    def __init__(self, name: str, extra_includes: List[str], logs_path: str = "logs") -> None:
        super().__init__()

        self.logs_path: str = os.path.abspath(logs_path)
        self.name = name
        self.logger: logging.Logger = logging.getLogger(name)
        self.extra_includes: List[str] = extra_includes

        self.__set_formatter()

        self.__set_logger_handler()
        self.logger.addHandler(self.handler)
        self.__set_extra_includes()

    def __set_formatter(self):
        self.formatter = logging.Formatter(
            fmt=self.format,
            datefmt=self.datefmt
        )

    def __set_logger_handler(self):
        os.makedirs(os.path.join(self.logs_path, self.name), exist_ok=True)

        handler = RotatingFileHandler(
            os.path.join(self.logs_path, self.name, self.name+'.log'),
            maxBytes=10000,
            backupCount=3,
            encoding='utf-8',
            delay=False
        )
        handler.setFormatter(self.formatter)
        handler.setLevel(self.level)
        self.handler = handler

    def __set_extra_includes(self):
        for extra in self.extra_includes:
            logging.info("Setting log for extra, {}".format(extra))
            logging.getLogger(extra).addHandler(self.handler)
