from __future__ import unicode_literals, absolute_import

import pandas as pd
from datetime import datetime

from backend.tests.run_test import os, app, db
from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer
from backend.apps.sales.models.orders import Order

from backend.apps.masters.views.companies import CompanyProcess
from backend.apps.masters.views.customers import CustomerProcess
from backend.apps.sales.views.orders import OrderProcess

from backend.tests.base import BaseTestCase

class TestOrderProcess(BaseTestCase):
    
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
            
    def test_003_order_loaddata(self):
        with self.app.app_context():
            op = OrderProcess(Order, db=db, 
                    csv_name='Test task - Postgres - orders.csv')
            
            op.load_data()
            
            for data in self.csv_order:
                order = db.session.execute(
                    db.select(Order).filter_by(
                    order_name=data['order_name'])).scalar_one() 
                
                # assert order.created_at == datetime.strptime(data['created_at'], 
                #                 op.FORMAT_DATETIME)
                assert order.order_name == data['order_name']
                assert order.customer_id == data['customer_id']
                
    
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
            
    def test_006_delete_company(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Company.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
        
        
        
        
        
        
        
        
            
        
        
        
