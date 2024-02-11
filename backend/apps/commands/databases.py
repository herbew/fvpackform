from __future__ import unicode_literals, absolute_import

import logging, time

from datetime import datetime

from flask import current_app

from backend.run import db
from backend.logs import FILE_HANDLER

from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer
from backend.apps.sales.models.orders import Order
from backend.apps.sales.models.order_items import OrderItem
from backend.apps.stocks.models.deliveries import Delivery

from backend.apps.masters.views.companies import CompanyProcess
from backend.apps.masters.views.customers import CustomerProcess
from backend.apps.sales.views.orders import OrderProcess
from backend.apps.sales.views.order_items import OrderItemProcess
from backend.apps.stocks.views.deliveries import DeliveryProcess

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)


def database_populate(db=db):
    log.info("database_populate()__start ..")
    
    time.sleep(2)
    cp = CompanyProcess(Company, db=db, 
                    csv_name='Test task - Postgres - customer_companies.csv')
    cp.load_data()
    
    time.sleep(2)    
    cp = CustomerProcess(Customer, db=db, 
                csv_name='Test task - Postgres - customers.csv')
    cp.load_data()
    
    time.sleep(2)
    op = OrderProcess(Order, db=db, 
                csv_name='Test task - Postgres - orders.csv')
    op.load_data()
    
    time.sleep(2)
    op = OrderItemProcess(OrderItem, db=db, 
                csv_name='Test task - Postgres - order_items.csv')
    op.load_data()
    
    time.sleep(2)            
    dp = DeliveryProcess(Delivery, db=db, 
            csv_name='Test task - Postgres - deliveries.csv')
    dp.load_data()
    
    log.info("database_populate()__completed ..")
        


