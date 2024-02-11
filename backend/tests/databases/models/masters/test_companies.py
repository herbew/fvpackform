from __future__ import unicode_literals, absolute_import

from datetime import datetime

from backend.tests.run_test import os, app, db
from backend.apps.masters.models.companies import Company
from backend.tests.base import BaseTestCase

class TestCompany(BaseTestCase):
    
    company_data = dict(
            name=("Roga & Kopyta", "Roga & Kopyta UPDATED" )
        )
    
    def test_001_create_company(self):
        with self.app.app_context():
            company = Company(
                name=self.company_data['name'][0],
            )
            
            try:
                db.session.add(company)
                db.session.commit()
            except:
                db.session.rollback()
                
            company = db.session.execute(
                db.select(Company).filter_by(
                name=self.company_data['name'][0])).scalar_one()
                
            assert company.name == self.company_data['name'][0]
            
    def test_002_retrieve_company_serializer(self):
        with self.app.app_context():
            company = db.session.execute(
                    db.select(Company).filter_by(
                    name=self.company_data['name'][0])).scalar_one()
                    
            company_rest = company.to_dict()
                
            assert company_rest['id'] == company.id
            assert company_rest['name'] == company.name
            
    def test_003_update_company(self):
        with self.app.app_context():
            try:
                company = db.session.execute(
                    db.select(Company).filter_by(
                    name=self.company_data['name'][0])).scalar_one()
                
                ts_updated = datetime.now()
                
                company.name = self.company_data['name'][1]
                company.updated = ts_updated
                db.session.commit()
                
                assert company.name == self.company_data['name'][1]
                assert company.updated == ts_updated
            except:
                db.session.rollback()
                
    def test_004_delete_company(self):
        with self.app.app_context():
            company = db.session.execute(
                db.select(Company).filter_by(
                name=self.company_data['name'][1])).scalar_one()
            db.session.delete(company)
            
            try:
                db.session.commit()
                
                company = db.session.execute(
                db.select(Company).filter_by(
                name=self.company_data['name'][1])).one_or_none()
            
                assert company == None
            
            except:
                db.session.rollback()


            