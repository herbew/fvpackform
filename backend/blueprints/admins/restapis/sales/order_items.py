from __future__ import unicode_literals, absolute_import

import logging

from flask.views import MethodView

from backend.apps.sales.models.order_items import OrderItem

from backend.logs import FILE_HANDLER

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

