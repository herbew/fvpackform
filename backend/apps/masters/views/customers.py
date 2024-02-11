from __future__ import unicode_literals, absolute_import

import logging
import pandas as pd
from datetime import datetime


from backend.run import db
from backend.logs import FILE_HANDLER

from backend.apps.masters.models.companies import Company
from backend.apps.masters.models.customers import Customer
from backend.apps.masters.views import BaseProcess


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

class CustomerProcess(BaseProcess):
    
    column_titles = ('user_id', 'login', 'password', 'name', 
              'company_id', 'credit_cards')
    
    @property
    def csv_file(self):
        return self._csv_file
    
    def load_data(self):
        log.info("CustomerProcess__load_data()__start ..")
        
        # Set a data frame
        df = pd.read_csv(self._csv_file)
        
        # Read data frame
        for index, v in enumerate(df.values):
            user_id = df[self.column_titles[0]][index]
            login = df[self.column_titles[1]][index]
            password = df[self.column_titles[2]][index]
            name = df[self.column_titles[3]][index]
            company_id = df[self.column_titles[4]][index]
            credit_cards = df[self.column_titles[5]][index]
            
            try:
                company = self._db.session.execute(
                    self._db.select(Company).filter_by(
                    id=int(company_id))).scalar_one() 
                
                # Initial models
                customer = self._models(
                        user_id=user_id,
                        name=name,
                        username=login,
                        company_id=company.id,
                        credit_cards=credit_cards
                        )
            
                self._db.session.add(customer)
                self._db.session.commit()
                log.debug("""INSERT INTO master_customer
                    SET user_id = {}, name='{}', 
                    username='{}', company_id={},
                    credit_cards='{}'""".format(
                    user_id, name, login, company.id, credit_cards))
            except Exception as e:
                log.error(e)
                self._db.session.rollback()
                continue
            
            # Makesure set password
            customer = self._db.session.execute(
                    self._db.select(Customer).filter_by(
                    user_id=user_id)).scalar_one() 
                    
            if customer.password is None:
                
                ts_updated = datetime.now()
                customer.set_password(password)
                customer.updated = ts_updated
                customer.user_updated = "SYSTEM"
                self._db.session.commit()
                
                log.debug("""UPDATE masters_customer WHERE  user_id={}, 
                    SET password = '{}'""".format(
                    user_id, customer.password))
            
        log.info("CustomerProcess__load_data()__end ..")
        
        
        