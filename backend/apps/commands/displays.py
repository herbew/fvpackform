from __future__ import unicode_literals, absolute_import

import logging
from backend.logs import FILE_HANDLER

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)


def get_logger(msg):
    log.debug(f"def get_logger('{msg}')")
    log.info(f"def get_logger('{msg}')")
    log.warning(f"def get_logger('{msg}')")
    log.error(f"def get_logger('{msg}')")
    log.critical(f"def get_logger('{msg}')")
    
    print(f"def get_logger('{msg}')")