from __future__ import unicode_literals, absolute_import

import pandas as pd
from backend.tests.run_test import os, app, db
from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer

from backend.apps.masters.views.companies import CompanyProcess
from backend.apps.masters.views.customers import CustomerProcess

from backend.tests.base import BaseTestCase

class TestCompanyProcess(BaseTestCase):
    
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
                
                
    
    def test_001_company_loaddata(self):
        with self.app.app_context():
            cp = CompanyProcess(Company, db=db, 
                    csv_name='Test task - Postgres - customer_companies.csv')
            
            cp.load_data()
            
            for data in self.csv_company:
                company = db.session.execute(
                    db.select(Company).filter_by(
                    name=data['company_name'])).scalar_one()
                
                assert company.id == data['company_id']
                assert company.name == data['company_name']
                
    def test_002_customer_loaddata(self):
        with self.app.app_context():
            cp = CustomerProcess(Customer, db=db, 
                    csv_name='Test task - Postgres - customers.csv')
            
            cp.load_data()
            
            for data in self.csv_customer:
                customer = db.session.execute(
                    db.select(Customer).filter_by(
                    user_id=data['user_id'])).scalar_one()
                
                assert customer.user_id == data['user_id']
                assert customer.name == data['name']
                assert customer.username == data['login']
                assert customer.company_id == int(data['company_id']) 
                assert customer.credit_cards == data['credit_cards']
                assert customer.check_password(data['password']) == True
    
    def test_003_delete_customer(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Customer.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
    
    def test_004_delete_company(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Company.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
        
        
    
        
        
        
        
        
        
            
        
        
        
