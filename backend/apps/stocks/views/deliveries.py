from __future__ import unicode_literals, absolute_import

import logging
import pandas as pd
import numpy as np

from datetime import datetime

from backend.run import db
from backend.logs import FILE_HANDLER

from backend.apps.sales.models.order_items import OrderItem
from backend.apps.stocks.models.deliveries import Delivery

from backend.apps.masters.views import BaseProcess

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)


class DeliveryProcess(BaseProcess):
    
    column_titles = ('id', 'order_item_id', 'delivered_quantity')
    
    @property
    def csv_file(self):
        return self._csv_file
    
    def load_data(self):
        log.info("DeliveryProcess__load_data()__start ..")
        
        # Set a data frame
        df = pd.read_csv(self._csv_file)
        
        # Read data frame
        for index, v in enumerate(df.values):
            delivery_id = df[self.column_titles[0]][index]
            order_item_id = df[self.column_titles[1]][index]
            delivered_quantity = df[self.column_titles[2]][index]
            
            try:
                delivered_quantity = int(delivered_quantity)
            except:
                delivered_quantity = 0
            
            if np.isnan(delivered_quantity): delivered_quantity = 0
            
            try:
                order_item = self._db.session.execute(
                    self._db.select(OrderItem).filter_by(
                    id=int(order_item_id))).scalar_one() 
                
                # Initial models
                delivery = self._models(
                    order_item_id=order_item.id, 
                    delivered_quantity=delivered_quantity)
            
                self._db.session.add(delivery)
                self._db.session.commit()
                log.debug("""INSERT INTO stock_delivery
                    SET id={}, order_item_id={}, delivered_quantity={}""".format(
                    delivery.id, order_item.id, delivered_quantity))
                
            except Exception as e:
                log.error(e)
                self._db.session.rollback()
                continue
            
            # Makesure id is same with resource
            delivery = self._db.session.execute(
                    self._db.select(Delivery).filter_by(
                    id=delivery.id)).scalar_one() 
                    
            old_delivery_id = delivery.id
            
            if delivery.id != int(delivery_id):
                
                ts_updated = datetime.now()
                
                delivery.id = int(delivery_id)
                delivery.updated = ts_updated
                delivery.user_updated = "SYSTEM"
                self._db.session.commit()
                
                log.debug("""UPDATE stock_delivery WHERE  id={} SET id = {}""".format(
                    old_delivery_id, delivery_id))
            
        log.info("DeliveryProcess__load_data()__end ..")
        
        
        