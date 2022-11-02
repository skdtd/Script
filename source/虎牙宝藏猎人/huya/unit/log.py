# coding: utf-8
import logging
import sys


class Log:
    file_handler = logging.FileHandler('log')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    logging.basicConfig(
        format='%(name)-45s %(asctime)s %(levelname)-8s | %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        level=logging.INFO,
        handlers=[
            file_handler,
            stream_handler
        ]
    )
    logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    @staticmethod
    def info(msg):
        logging.info(msg)

    @staticmethod
    def debug(msg):
        logging.debug(msg)

    @staticmethod
    def warning(msg):
        logging.warning(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)

    @staticmethod
    def critical(msg):
        logging.critical(msg)
