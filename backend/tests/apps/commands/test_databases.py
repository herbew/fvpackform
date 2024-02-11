from __future__ import unicode_literals, absolute_import

from backend.tests.run_test import os, app, db

from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer
from backend.apps.sales.models.orders import Order
from backend.apps.sales.models.order_items import OrderItem
from backend.apps.stocks.models.deliveries import Delivery

from backend.apps.commands.databases import database_populate

from backend.tests.base import BaseTestCase

class TestDeliveryProcess(BaseTestCase):
    def xtest_001_database_populate(self):
        with self.app.app_context():
             database_populate(db)
            
            
    def test_002_delete_delivery(self):
        with self.app.app_context():
             # Delete data test
            delete_all = Delivery.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_003_delete_order_item(self):
        with self.app.app_context():
             # Delete data test
            delete_all = OrderItem.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_004_delete_order(self):
        with self.app.app_context():
             # Delete data test
            delete_all = Order.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
    
    def test_005_delete_customer(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Customer.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_06_delete_company(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Company.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
    