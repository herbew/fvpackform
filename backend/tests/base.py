from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from backend.tests.run_test import os, app, db

class BaseTestCase(TestCase):
    def create_app(self):
        return app
    
    def setUp(self):  # done in our pytest fixture before yield
        self.app = self.create_app()
        
        with self.app.app_context():
            # db create
            db.create_all()
            db.session.commit()
            
        
    def tearDown(self): # done in our pytest fixture after yield
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
