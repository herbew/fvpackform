from __future__ import unicode_literals, absolute_import

import logging

from flask import Blueprint, url_for, redirect
from flask.views import MethodView

from backend.apps.sales.models.order_items import OrderItem
from backend.apps.sales.apis.order_items import (
    OrderItemListMethodView as MasterOrderItemListMethodView
    )


from backend.logs import FILE_HANDLER

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

admin_api_sales_order_item = Blueprint("admin_api_sales_order_item", __name__)

class AdminApiOrderItemListMethodView(MasterOrderItemListMethodView):
    pass

admin_api_sales_order_item.add_url_rule(
    "order/item/list/",
    view_func=AdminApiOrderItemListMethodView.as_view("order_item_list"))