from __future__ import unicode_literals, absolute_import

import logging
import pandas as pd
import numpy as np

from datetime import datetime


from backend.run import db
from backend.logs import FILE_HANDLER

from backend.apps.sales.models.orders import Order
from backend.apps.sales.models.order_items import OrderItem

from backend.apps.masters.views import BaseProcess


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)



class OrderItemProcess(BaseProcess):
    
    column_titles = ('id', 'order_id', 'price_per_unit', 'quantity', 'product')
    
    @property
    def csv_file(self):
        return self._csv_file
    
    def load_data(self):
        log.info("OrderItemProcess__load_data()__start ..")
        
        # Set a data frame
        df = pd.read_csv(self._csv_file)
        
        # Read data frame
        for index, v in enumerate(df.values):
            order_item_id = df[self.column_titles[0]][index]
            order_id = df[self.column_titles[1]][index]
            price_per_unit = df[self.column_titles[2]][index]
            quantity = df[self.column_titles[3]][index]
            product = df[self.column_titles[4]][index]
            
            try:
                price_per_unit = float(price_per_unit)
            except:
                price_per_unit = 0.0
            
            if np.isnan(price_per_unit): price_per_unit = 0.0
            
            
            try:
                quantity = int(quantity)
            except:
                quantity = 0
            
            if np.isnan(quantity): quantity = 0
            
            try:
                order = self._db.session.execute(
                    self._db.select(Order).filter_by(
                    id=int(order_id))).scalar_one() 
                
                # Initial models
                order_item = self._models(
                    order_id=order.id, 
                    price_per_unit=price_per_unit, 
                    quantity=quantity,
                    product=product)
            
                self._db.session.add(order_item)
                self._db.session.commit()
                log.debug("""INSERT INTO sales_orderitem
                    SET id={}, order_id={}, price_per_unit={}, 
                    quantity={}, product='{}'""".format(
                    order_item.id, order.id, price_per_unit, 
                    quantity, product))
                
            except Exception as e:
                log.error(e)
                self._db.session.rollback()
                continue
            
            # Makesure id is same with resource
            order_item = self._db.session.execute(
                    self._db.select(OrderItem).filter_by(
                    order_id=order.id, product=product)).scalar_one() 
                    
            old_order_item_id = order_item.id
            
            if order_item.id != int(order_item_id):
                
                ts_updated = datetime.utcnow()
                
                order_item.id = int(order_item_id)
                order_item.updated = ts_updated
                order_item.user_updated = "SYSTEM"
                self._db.session.commit()
                
                log.debug("""UPDATE sales_orderitem WHERE  id={}, order_id='{}', 
                    product='{}' SET id = {}""".format(
                    old_order_item_id, order_id, product, order_item_id))
            
        log.info("OrderItemProcess__load_data()__end ..")
        
        
        