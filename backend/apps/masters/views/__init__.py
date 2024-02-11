from __future__ import unicode_literals, absolute_import

import logging, os

from flask import current_app

from backend.logs import FILE_HANDLER
from backend.run import db

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

class BaseProcess(object):
    def __init__(self, models, db=db, csv_name=""):
        self._db = db
        self._csv_file = os.path.join(current_app.static_folder,'database',
                    'test_data', csv_name)
        self._models = models
        
    def load_data(self):
        pass


