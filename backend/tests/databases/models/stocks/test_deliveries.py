from __future__ import unicode_literals, absolute_import

from datetime import datetime

import pandas as pd
import numpy as np

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

class TestDelivery(BaseTestCase):
    
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
        
    def test_005_create_delivery(self):
        with self.app.app_context():
            
            # Get first a order data
            data = self.csv_delivery[0]
            
            try:
                delivered_quantity = int(delivered_quantity)
            except:
                delivered_quantity = 0
            
            if np.isnan(delivered_quantity): delivered_quantity = 0
                
            try:
                order_item = db.session.execute(
                    db.select(OrderItem).filter_by(
                    id=int(data['order_item_id']))).scalar_one() 
                
                # set OrderItem models
                delivery = Delivery(
                     order_item_id=order_item.id, 
                     delivered_quantity=delivered_quantity
                    )
                
                db.session.add(delivery)
            
                db.session.commit()
            except:
                raise
                db.session.rollback()
                return
            
            # update id
            delivery = db.session.execute(
                    db.select(Delivery).filter_by(
                    id=delivery.id)).scalar_one() 
                    
            old_delivery_id = delivery.id
            
            if delivery.id != int(data['delivery_id']):
                
                ts_updated = datetime.utcnow()
                
                delivery.id = int(data['delivery_id'])
                delivery.updated = ts_updated
                delivery.user_updated = "SYSTEM"
                db.session.commit()
                
            assert delivery.id == int(data['delivery_id'])
            assert delivery.order_item_id == delivery.order_item.id
            assert int(delivery.delivered_quantity) == delivered_quantity
    
    
    def xtest_006_retrieve_delivery_serializer(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_delivery[0]
            
            delivery = db.session.execute(
                    db.select(Delivery).filter_by(
                    id=int(data['delivery_id']))).scalar_one() 
            
            delivery_rest = delivery.to_dict()
            
            # serialize_only = ('id', 'delivered_quantity', 'order_item')
            
            assert delivery_rest['id'] == delivery.id
            assert delivery_rest['delivered_quantity'] == delivery.delivered_quantity
            
            assert delivery_rest['order_item']['id'] == delivery.order_item.id 
            assert float(delivery_rest['order_item']['price_per_unit']) == float(delivery.order_item.price_per_unit) 
            assert int(delivery_rest['order_item']['quantity']) == int(delivery.order_item.quantity) 
            assert delivery_rest['order_item']['product'] == delivery.order_item.product
            
            assert delivery_rest['order_item']['order']['id'] == delivery.order_item.order.id
            #assert datetime.strptime(delivery_rest['order_item']['order']['created_at'], self.FORMAT_DATETIME) == delivery.order_item.order.created_at
            assert delivery_rest['order_item']['order']['order_name'] == delivery.order_item.order.order_name
            
            assert delivery_rest['order_item']['order']['customer']['user_id'] == delivery.order_item.order.customer.user_id
            assert delivery_rest['order_item']['order']['customer']['name'] == delivery.order_item.order.customer.name
            assert delivery_rest['order_item']['order']['customer']['username'] == delivery.order_item.order.customer.username
            assert delivery_rest['order_item']['order']['customer']['credit_cards'] == delivery.order_item.order.customer.credit_cards
            
            assert delivery_rest['order_item']['order']['customer']['company']['id'] == delivery.order_item.order.customer.company.id
            assert delivery_rest['order_item']['order']['customer']['company']['name'] == delivery.order_item.order.customer.company.name
                    
                    
    def test_007_update_delivery(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_delivery[0]
                
            delivered_quantity = 1000
                
            delivery = db.session.execute(
                    db.select(Delivery).filter_by(
                    id=int(data['delivery_id']))).scalar_one() 
            
            ts_updated = datetime.utcnow()
            
            delivery.delivered_quantity = delivered_quantity
            delivery.updated = ts_updated
            delivery.user_updated = "SYSTEM"
            db.session.commit()
            
            assert delivery.id == int(data['delivery_id'])
            assert delivery.order_item_id == int(data['order_item_id'])
            assert int(delivery.delivered_quantity) == delivered_quantity
            #assert delivery.updated == ts_updated
            assert delivery.user_updated == "SYSTEM"
    
            
    def test_008_delete_delivery(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_delivery[0]
            
            print(int(data['delivery_id']))
            
            delivery = db.session.execute(
                    db.select(Delivery).filter_by(
                    id=int(data['delivery_id']))).scalar_one() 
                    
            db.session.delete(delivery)
            try:
                db.session.commit()
                
                delivery = db.session.execute(
                    db.select(Delivery).filter_by(
                    id=int(data['delivery_id']))).one_or_none()
            
                assert delivery == None
            
            except:
                db.session.rollback()
                
    
    def test_009_delete_order_item(self):
        with self.app.app_context():
            # Delete data test
            delete_all = OrderItem.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_010_delete_order(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Order.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_011_delete_customer(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Customer.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    def test_012_delete_company(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Company.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
    
        
        
        
        
        
        
        
            
        
        
        
