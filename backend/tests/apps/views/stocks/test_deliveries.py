from __future__ import unicode_literals, absolute_import

import pandas as pd
import numpy as np
from datetime import datetime

from backend.tests.run_test import os, app, db
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

from backend.tests.base import BaseTestCase

class TestDeliveryProcess(BaseTestCase):
    
    def setUp(self):
        self.app = self.create_app()
        
        with self.app.app_context():
            # db create
            db.create_all()
            db.session.commit()
            
            
            # csv company
            self.csv_company = []
            cp = CompanyProcess(Company, db=db, 
                    csv_name='Test task - Postgres - customer_companies.csv')
            
            df = pd.read_csv(cp.csv_file)
            
            # Read data frame of csv company
            for index, v in enumerate(df.values):
                
                self.csv_company.append(
                    dict(
                        company_id = df[cp.column_titles[0]][index],
                        company_name = df[cp.column_titles[1]][index]
                        ))
            
            # csv custormer
            self.csv_customer = []
            cp = CustomerProcess(Customer, db=db, 
                    csv_name='Test task - Postgres - customers.csv')
            
            df = pd.read_csv(cp.csv_file)
            
            # Read data frame of csv customer
            for index, v in enumerate(df.values):
                self.csv_customer.append(
                    dict(
                        user_id=df[cp.column_titles[0]][index],
                        login=df[cp.column_titles[1]][index],
                        password=df[cp.column_titles[2]][index],
                        name=df[cp.column_titles[3]][index],
                        company_id=df[cp.column_titles[4]][index],
                        credit_cards=df[cp.column_titles[5]][index]))
                
            # csv order
            self.csv_order = []
            op = OrderProcess(Order, db=db, 
                    csv_name='Test task - Postgres - orders.csv')
            
            df = pd.read_csv(op.csv_file)
            
            # Read data frame of csv order
            for index, v in enumerate(df.values):
                self.csv_order.append(
                    dict(
                        order_id=df[op.column_titles[0]][index],
                        created_at=df[op.column_titles[1]][index],
                        order_name=df[op.column_titles[2]][index],
                        customer_id=df[op.column_titles[3]][index]))
            
            # csv order item
            self.csv_order_item = []
            op = OrderItemProcess(OrderItem, db=db, 
                    csv_name='Test task - Postgres - order_items.csv')
            
            df = pd.read_csv(op.csv_file)
            
            # Read data frame of csv order
            for index, v in enumerate(df.values):
                self.csv_order_item.append(
                    dict(
                        order_item_id=df[op.column_titles[0]][index],
                        order_id=df[op.column_titles[1]][index],
                        price_per_unit=df[op.column_titles[2]][index] if not np.isnan(df[op.column_titles[2]][index]) else 0.0,
                        quantity=df[op.column_titles[3]][index] if not np.isnan(df[op.column_titles[3]][index]) else 0,
                        product=df[op.column_titles[4]][index]))
            
            # csv delivery
            self.csv_delivery = []
            dp = DeliveryProcess(Delivery, db=db, 
                    csv_name='Test task - Postgres - deliveries.csv')
            
            df = pd.read_csv(dp.csv_file)
            
            # Read data frame of csv order
            for index, v in enumerate(df.values):
                self.csv_delivery.append(
                    dict(
                        delivery_id=df[dp.column_titles[0]][index],
                        order_item_id=df[dp.column_titles[1]][index],
                        delivered_quantity=df[dp.column_titles[2]][index] if not np.isnan(df[dp.column_titles[2]][index]) else 0
                        ))    
                
    
    def test_001_company_loaddata(self):
        with self.app.app_context():
            cp = CompanyProcess(Company, db=db, 
                        csv_name='Test task - Postgres - customer_companies.csv')
            cp.load_data()
        
    def test_002_customer_loaddata(self):
        with self.app.app_context():
            cp = CustomerProcess(Customer, db=db, 
                        csv_name='Test task - Postgres - customers.csv')
            cp.load_data()
        
    def test_003_order_loaddata(self):
        with self.app.app_context():
            op = OrderProcess(Order, db=db, 
                        csv_name='Test task - Postgres - orders.csv')
            op.load_data()
    
    def test_004_order_item_loaddata(self):
        with self.app.app_context():
            op = OrderItemProcess(OrderItem, db=db, 
                        csv_name='Test task - Postgres - order_items.csv')
            op.load_data()
                
    def test_005_delivery_loaddata(self):
        with self.app.app_context():
            dp = DeliveryProcess(Delivery, db=db, 
                    csv_name='Test task - Postgres - deliveries.csv')
            
            dp.load_data()
            
            for data in self.csv_delivery:
                delivery = db.session.execute(
                    db.select(Delivery).filter_by(
                    id=int(data['delivery_id']))).scalar_one()   
                
                try:
                    delivered_quantity = int(data['delivered_quantity'])
                except:
                    delivered_quantity = 0
                
                if np.isnan(delivered_quantity): delivered_quantity = 0
            
                assert delivery.id == int(data['delivery_id'])
                assert delivery.order_item_id == int(data['order_item_id'])
                assert int(delivery.delivered_quantity) == delivered_quantity
    
    def test_006_delete_delivery(self):
        with self.app.app_context():
             # Delete data test
            delete_all = Delivery.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_007_delete_order_item(self):
        with self.app.app_context():
             # Delete data test
            delete_all = OrderItem.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_008_delete_order(self):
        with self.app.app_context():
             # Delete data test
            delete_all = Order.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
    
    def test_009_delete_customer(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Customer.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_010_delete_company(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Company.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
        
        
        
        
        
        
        
        
            
        
        
        