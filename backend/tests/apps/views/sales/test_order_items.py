from __future__ import unicode_literals, absolute_import

import pandas as pd
import numpy as np
from datetime import datetime

from backend.tests.run_test import os, app, db
from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer
from backend.apps.sales.models.orders import Order
from backend.apps.sales.models.order_items import OrderItem

from backend.apps.masters.views.companies import CompanyProcess
from backend.apps.masters.views.customers import CustomerProcess
from backend.apps.sales.views.orders import OrderProcess
from backend.apps.sales.views.order_items import OrderItemProcess

from backend.tests.base import BaseTestCase

class TestOrderItemProcess(BaseTestCase):
    
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
            
            for data in self.csv_order_item:
                order_item = db.session.execute(
                    db.select(OrderItem).filter_by(
                    id=int(data['order_item_id']))).scalar_one()  
                
                assert order_item.id == int(data['order_item_id'])
                assert order_item.order_id == int(data['order_id'])
                assert float(order_item.price_per_unit) == round(float(data['price_per_unit']), 2)
                assert order_item.quantity == int(data['quantity'])
                assert order_item.product == data['product']
                
    def test_005_delete_order_item(self):
        with self.app.app_context():
             # Delete data test
            delete_all = OrderItem.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_006_delete_order(self):
        with self.app.app_context():
             # Delete data test
            delete_all = Order.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
    
    def test_007_delete_customer(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Customer.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_008_delete_company(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Company.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
        
        
        
        
        
        
        
        
            
        
        
        