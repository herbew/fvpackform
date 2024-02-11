from __future__ import unicode_literals, absolute_import

import logging

from flask import jsonify
from backend.logs import FILE_HANDLER

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

def welcome():
    """
        - methods : GET
        - read() : Display welcome sessage
        - parameters input :
            -- None
        - return jsonify(data) -- success - 200
    """
    message = dict(
            title='Welcome', 
            desc='Welcome to PackForm')
    
    return jsonify(message), 200