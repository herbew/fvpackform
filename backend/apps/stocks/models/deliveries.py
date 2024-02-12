from __future__ import unicode_literals, absolute_import

import logging
from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from backend.run import db

from backend.logs import FILE_HANDLER

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)


class Delivery(db.Model, SerializerMixin):
    """
        Models    : Delivery
        Table     : stocks_delivery
        Fields    :
                - id                 -- Integer
                - order_item_id      -- Integer  
                - delivered_quantity -- Integer
                
        
    """
    __tablename__ = 'stocks_delivery'
    
    serialize_only = ('id', 'delivered_quantity', 'order_item')
    
    id = db.Column(db.Integer, primary_key=True)
    order_item_id = db.Column(db.Integer, 
                    db.ForeignKey("sales_orderitem.id", ondelete='RESTRICT'))
    delivered_quantity = db.Column(db.Integer, nullable=False, default=0)
    
    # Tracer fields
    created = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    updated = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    user_updated = db.Column(db.String(30),  default="Admin")
    
    
    # Relationships 
    
    # Populate relate to field OrderItem.deliveries
    order_item = db.relationship("OrderItem", back_populates="deliveries")

    def __init__(self, 
                 order_item_id, 
                 delivered_quantity):
        
        self.order_item_id = order_item_id
        self.delivered_quantity = delivered_quantity

    def __repr__(self):
        return '''<id:{}, order_item_id:{}, delivered_quantity:{}'''.format(
            self.id, self.order_item_id, self.delivered_quantity)
    
    


