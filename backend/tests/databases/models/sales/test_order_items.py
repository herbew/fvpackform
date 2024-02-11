from __future__ import unicode_literals, absolute_import

from datetime import datetime

import pandas as pd
import numpy as np

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

class TestOrderItem(BaseTestCase):
    
    FORMAT_DATETIME = "%Y-%m-%d %H:%M:%S"
    
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
        
    def test_004_create_order_item(self):
        with self.app.app_context():
            
            # Get first a order data
            data = self.csv_order_item[0]
            
            try:
                price_per_unit = float(data['price_per_unit'])
            except:
                price_per_unit = 0.0
                
            try:
                quantity = int(data['quantity'])
            except:
                quantity = 0
                
            try:
                order = db.session.execute(
                    db.select(Order).filter_by(
                    id=int(data['order_id']))).scalar_one()
                
                # set OrderItem models
                order_item = OrderItem(
                     order_id=order.id, 
                     price_per_unit=price_per_unit, 
                     quantity=quantity,
                     product=data['product']
                    )
                
                db.session.add(order_item)
            
                db.session.commit()
            except:
                db.session.rollback()
                return
            
            # update id
            order_item = db.session.execute(
                    db.select(OrderItem).filter_by(
                    order_id=order.id, product=data['product'])).scalar_one() 
                
            old_order_item_id = order_item.id
            
            if order_item.id != int(data['order_item_id']):
                ts_updated = datetime.now()
                
                order_item.id = int(data['order_item_id'])
                order_item.updated = ts_updated
                order_item.user_updated = "SYSTEM"
                db.session.commit()
                
            assert order_item.order_id == order.id
            assert float(order_item.price_per_unit) == round(price_per_unit,2) 
            assert int(order_item.quantity) == quantity
            assert order_item.product == data['product']
            
    def test_005_retrieve_order_item_serializer(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_order_item[0]
            
            order_item = db.session.execute(
                    db.select(OrderItem).filter_by(
                    id=int(data['order_item_id']))).scalar_one()
            
            order_item_rest = order_item.to_dict()
            
            # serialize_only = ('id', 'price_per_unit', 'quantity', 'product', 'order')
            assert order_item_rest['id'] == order_item.id 
            assert float(order_item_rest['price_per_unit']) == float(order_item.price_per_unit) 
            assert int(order_item_rest['quantity']) == int(order_item.quantity) 
            assert order_item_rest['product'] == order_item.product
            
            assert order_item_rest['order']['id'] == order_item.order.id
            assert datetime.strptime(order_item_rest['order']['created_at'], self.FORMAT_DATETIME) == order_item.order.created_at
            assert order_item_rest['order']['order_name'] == order_item.order.order_name
            
            assert order_item_rest['order']['customer']['user_id'] == order_item.order.customer.user_id
            assert order_item_rest['order']['customer']['name'] == order_item.order.customer.name
            assert order_item_rest['order']['customer']['username'] == order_item.order.customer.username
            assert order_item_rest['order']['customer']['credit_cards'] == order_item.order.customer.credit_cards
            
            assert order_item_rest['order']['customer']['company']['id'] == order_item.order.customer.company.id
            assert order_item_rest['order']['customer']['company']['name'] == order_item.order.customer.company.name
            
            
    def test_006_update_order_item(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_order_item[0]
            
            try:
                price_per_unit = float(data['price_per_unit'])
            except:
                price_per_unit = 0.0
                
            try:
                quantity = int(data['quantity'])
            except:
                quantity = 0
                
            order_item = db.session.execute(
                    db.select(OrderItem).filter_by(
                    id=int(data['order_item_id']))).scalar_one() 
            
            ts_updated = datetime.now()
            
            order_item.product = "{} UPDATED".format(data['product'])
            order_item.updated = ts_updated
            order_item.user_updated = "SYSTEM"
            db.session.commit()
            
            assert order_item.order_id == int(data["order_id"])
            assert float(order_item.price_per_unit) == round(price_per_unit,2) 
            assert int(order_item.quantity) == quantity
            assert order_item.product == "{} UPDATED".format(data['product'])
            assert order_item.updated == ts_updated
            assert order_item.user_updated == "SYSTEM"
    
    def test_007_delete_order_item(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_order_item[0]
            
            order_item = db.session.execute(
                    db.select(OrderItem).filter_by(
                    id=int(data['order_item_id']))).scalar_one()
                    
            db.session.delete(order_item)
            try:
                db.session.commit()
                
                order_item = db.session.execute(
                    db.select(OrderItem).filter_by(
                    id=int(data['order_item_id']))).one_or_none()
            
                assert order_item == None
            
            except:
                db.session.rollback()
    
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
            
    
        
        
        
        
        
        
        
            
        
        
        
