from __future__ import unicode_literals, absolute_import

from datetime import datetime

import pandas as pd
from backend.tests.run_test import os, app, db
from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer

from backend.apps.masters.views.companies import CompanyProcess
from backend.apps.masters.views.customers import CustomerProcess

from backend.tests.base import BaseTestCase

class TestCustomer(BaseTestCase):
    
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
            
    def test_002_create_customer(self):
        with self.app.app_context():
            
            # Get first a customer data
            data = self.csv_customer[0]
            try:
                company = db.session.execute(
                        db.select(Company).filter_by(
                        id=int(data['company_id']))).scalar_one()
                        
                # set Customer models
                customer = Customer(
                    user_id=data['user_id'], 
                    name=data['name'], 
                    username=data['login'],  
                    company_id=company.id, 
                    credit_cards=data['credit_cards']
                    )
                
                db.session.add(customer)
                db.session.commit()
            except:
                db.session.rollback()
                return
            
            # update password
            customer = db.session.execute(
                db.select(Customer).filter_by(
                user_id=data['user_id'])).scalar_one()
                
            if customer.password is None:
                ts_updated = datetime.utcnow()
                customer.set_password(data['password'])
                customer.updated = ts_updated
                db.session.commit()
                
            assert customer.user_id == data['user_id']
            assert customer.name == data['name']
            assert customer.username == data['login']
            assert customer.company_id == company.id 
            assert customer.credit_cards == data['credit_cards']
            assert customer.check_password(data['password']) == True
    
    def test_002_retrieve_customer_serializer(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_customer[0]
            
            customer = db.session.execute(
                db.select(Customer).filter_by(
                user_id=data['user_id'])).scalar_one()
                
            customer_rest = customer.to_dict()
            
            assert customer_rest['user_id'] == customer.user_id
            assert customer_rest['name'] == customer.name
            assert customer_rest['username'] == customer.username
            assert customer_rest['credit_cards'] == customer.credit_cards
            
            assert customer_rest['company']['id'] == customer.company.id
            assert customer_rest['company']['name'] == customer.company.name
            
            
    def test_004_update_customer(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_customer[0]
            
            customer = db.session.execute(
                db.select(Customer).filter_by(
                user_id=data['user_id'])).scalar_one()
            
            ts_updated = datetime.utcnow()
            
            customer.name = "{} UPDATED".format(data['name'])
            customer.updated = ts_updated
            db.session.commit()
            
            assert customer.user_id == data['user_id']
            assert customer.name == "{} UPDATED".format(data['name'])
            assert customer.username == data['login']
            assert customer.company_id == int(data['company_id'])
            assert customer.credit_cards == data['credit_cards']
            assert customer.check_password(data['password']) == True
    
    def test_005_delete_customer(self):
        with self.app.app_context():
            # Get first a customer data
            data = self.csv_customer[0]
            
            customer = db.session.execute(
                db.select(Customer).filter_by(
                user_id=data['user_id'])).scalar_one()
            db.session.delete(customer)
            try:
                db.session.commit()
                
                customer = db.session.execute(
                db.select(Customer).filter_by(
                user_id=data['user_id'])).one_or_none()
            
                assert customer == None
            
            except:
                db.session.rollback()
    
    def test_006_delete_company(self):
        with self.app.app_context():
            # Delete data test
            delete_all = Company.__table__.delete()
            db.session.execute(delete_all)
            db.session.commit()
            
   
        
        
        
        
        
        
        
        
            
        
        
        
