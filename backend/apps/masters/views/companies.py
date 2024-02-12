from __future__ import unicode_literals, absolute_import

import logging
import pandas as pd
from datetime import datetime


from backend.run import db
from backend.logs import FILE_HANDLER

from backend.apps.masters.models.companies import Company
from backend.apps.masters.views import BaseProcess


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

class CompanyProcess(BaseProcess):
    
    column_titles = ('company_id', 'company_name')
    
    @property
    def csv_file(self):
        return self._csv_file
    
    def load_data(self):
        log.info("CompanyProcess__load_data()__start ..")
        
        # Set a data frame
        df = pd.read_csv(self._csv_file)
        
        # Read data frame
        for index, v in enumerate(df.values):
            company_id = df[self.column_titles[0]][index]
            company_name = df[self.column_titles[1]][index]
            
            # Initial models
            company = self._models(
                    name=company_name
                    )
            
            try:
                self._db.session.add(company)
                self._db.session.commit()
                log.debug("""INSERT INTO master_company 
                    SET id = {}, name='{}'""".format(
                    company_id, company_name))
            except Exception as e:
                log.error(e)
                self._db.session.rollback()
                continue
            
            # Makesure id is same with resource
            company = self._db.session.execute(
                    self._db.select(Company).filter_by(
                    name=company_name)).scalar_one() 
                    
            old_company_id = company.id
            
            if company.id != int(company_id):
                
                ts_updated = datetime.utcnow()
                
                company.id = int(company_id)
                company.updated = ts_updated
                company.user_updated = "SYSTEM"
                self._db.session.commit()
                
                log.debug("""UPDATE masters_company WHERE  id={}, name='{}'
                    SET id = {}""".format(
                    old_company_id, company_name, company_id))
            
        log.info("CompanyProcess__load_data()__end ..")
        
        
        