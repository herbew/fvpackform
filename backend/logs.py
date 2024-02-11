from __future__ import unicode_literals, absolute_import

import logging

from logging.handlers import RotatingFileHandler

FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


FILE_HANDLER = logging.FileHandler(filename='/tmp/flasks_backend_record.log')
FILE_HANDLER.setFormatter(FORMATTER)

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)

TESTING_FILE_HANDLER = logging.FileHandler(filename='/tmp/tests_flasks_backend_record.log')
TESTING_FILE_HANDLER.setFormatter(FORMATTER)

ROTATING_FILE_HANDLER = RotatingFileHandler(
        '/tmp/flasks_backend_record.log',
        mode='a',
        maxBytes=5*1024*1024,
        backupCount=10,
        encoding=None,
        delay=0
    )

