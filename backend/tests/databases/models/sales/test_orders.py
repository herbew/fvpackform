from __future__ import unicode_literals, absolute_import

from datetime import datetime

import pandas as pd
from backend.tests.run_test import os, app, db

from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer
from backend.apps.sales.models.orders import Order

from backend.apps.masters.views.companies import CompanyProcess
from backend.apps.masters.views.customers import CustomerProcess
from backend.apps.sales.views.orders import OrderProcess

from backend.tests.base import BaseTestCase

class TestOrder(BaseTestCase):
    
    FORMAT_DATETIME = "%Y-%m-%dT%H:%M:%SZ"
    FORMAT_DATETIME_1 = "%Y-%m-%d %H:%M:%S"
    
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
        
    def test_003_create_order(self):
        with self.app.app_context():
            
            # Get first a order data
            data = self.csv_order[0]
            
            try:
                customer = db.session.execute(
                    db.select(Customer).filter_by(
                    user_id=data['customer_id'])).scalar_one()
                    
                # set Order models
                order = Order(
                    created_at=datetime.strptime(data['created_at'], 
                                    self.FORMAT_DATETIME),
                    order_name=data['order_name'],
                    customer_id=customer.user_id
                    )
                
                db.session.add(order)
            
                db.session.commit()
            except:
                db.session.rollback()
                return
            
            # update id
            order = db.session.execute(
                    db.select(Order).filter_by(
                    order_name=data['order_name'])).scalar_one() 
                
            old_order_id = order.id
            
            if order.id != int(data['order_id']):
                ts_updated = datetime.now()
                
                order.id = int(data['order_id'])
                order.updated = ts_updated
                order.user_updated = "SYSTEM"
                db.session.commit()
                
            assert order.created_at == datetime.strptime(data['created_at'], 
                                self.FORMAT_DATETIME)
            assert order.order_name == data['order_name']
            assert order.customer_id == customer.user_id
    
    def test_004_retrieve_order_serializer(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_order[0]
            order = db.session.execute(
                    db.select(Order).filter_by(
                    order_name=data['order_name'])).scalar_one() 
                    
            order_rest = order.to_dict()
            
            # serialize_only = ('id', 'created_at', 'order_name', 'customer')
            assert order_rest['id'] == order.id
            assert datetime.strptime(order_rest['created_at'], self.FORMAT_DATETIME_1) == order.created_at
            assert order_rest['order_name'] == order.order_name
            
            assert order_rest['customer']['user_id'] == order.customer.user_id
            assert order_rest['customer']['name'] == order.customer.name
            assert order_rest['customer']['username'] == order.customer.username
            assert order_rest['customer']['credit_cards'] == order.customer.credit_cards
            
            assert order_rest['customer']['company']['id'] == order.customer.company.id
            assert order_rest['customer']['company']['name'] == order.customer.company.name
            
            
    def test_005_update_order(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_order[0]
            
            order = db.session.execute(
                    db.select(Order).filter_by(
                    order_name=data['order_name'])).scalar_one() 
            
            ts_updated = datetime.now()
            
            order.name = "{} UPDATED".format(data['order_name'])
            order.updated = ts_updated
            order.user_updated = "SYSTEM"
            db.session.commit()
            
            assert order.created_at == datetime.strptime(data['created_at'], 
                                self.FORMAT_DATETIME)
            assert order.order_name == data['order_name']
            assert order.customer_id == data['customer_id']
            assert order.updated == ts_updated
            assert order.user_updated == "SYSTEM"
    
    def test_006_delete_order(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_order[0]
            
            order = db.session.execute(
                    db.select(Order).filter_by(
                    order_name=data['order_name'])).scalar_one() 
                    
            db.session.delete(order)
            try:
                db.session.commit()
                
                order = db.session.execute(
                    db.select(Order).filter_by(
                    order_name=data['order_name'])).one_or_none()
            
                assert order == None
            
            except:
                db.session.rollback()
    
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
            
    
        
        
        
        
        
        
        
            
        
        
        