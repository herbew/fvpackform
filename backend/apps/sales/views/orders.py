from __future__ import unicode_literals, absolute_import

import logging, pytz
import pandas as pd
from datetime import datetime


from backend.run import db, os
from backend.logs import FILE_HANDLER

from backend.apps.masters.models.customers import Customer
from backend.apps.sales.models.orders import Order

from backend.apps.masters.views import BaseProcess


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)



class OrderProcess(BaseProcess):
    
    FORMAT_DATETIME = "%Y-%m-%dT%H:%M:%SZ" #2020-01-15T17:34:12Z
    column_titles = ('id', 'created_at', 'order_name', 'customer_id')
    
    @property
    def csv_file(self):
        return self._csv_file
    
    def load_data(self):
        log.info("OrderProcess__load_data()__start ..")
        
        # Set a data frame
        df = pd.read_csv(self._csv_file)
        
        # Read data frame
        for index, v in enumerate(df.values):
            order_id = df[self.column_titles[0]][index]
            created_at = df[self.column_titles[1]][index]
            order_name = df[self.column_titles[2]][index]
            customer_id = df[self.column_titles[3]][index]
            
            try:
                customer = self._db.session.execute(
                    self._db.select(Customer).filter_by(
                    user_id=customer_id)).scalar_one() 
                
                # Initial models
                local_datetime = datetime.strptime(created_at, self.FORMAT_DATETIME)
                
                # Convert to UTC
                utc_string = local_datetime.astimezone(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
                utc_datetime = datetime.strptime(utc_string,'%Y-%m-%d %H:%M:%S %Z%z')
                
                order = self._models(
                        created_at=utc_datetime,
                        order_name=order_name,
                        customer_id=customer.user_id,
                        )
            
                self._db.session.add(order)
                self._db.session.commit()
                log.debug("""INSERT INTO sales_order
                    SET id={}, created_at={}, order_name='{}', 
                    customer_id='{}'""".format(
                    order.id, created_at, order_name, customer.user_id))
            except Exception as e:
                log.error(e)
                self._db.session.rollback()
                continue
            
            # Makesure id is same with resource
            order = self._db.session.execute(
                    self._db.select(Order).filter_by(
                    order_name=order_name)).scalar_one() 
                    
            old_order_id = order.id
            
            if order.id != int(order_id):
                
                ts_updated = datetime.utcnow()
                
                order.id = int(order_id)
                order.updated = ts_updated
                order.user_updated = "SYSTEM"
                self._db.session.commit()
                
                log.debug("""UPDATE sales_order WHERE  id={}, order_name='{}'
                    SET id = {}""".format(
                    old_order_id, order_name, order_id))
            
        log.info("OrderProcess__load_data()__end ..")
        
        
        