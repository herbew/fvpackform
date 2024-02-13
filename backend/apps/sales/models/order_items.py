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


class OrderItem(db.Model, SerializerMixin):
    """
        Models    : OrderItem
        Table     : sales_order
        Fields    :
                - id             -- Integer
                
                - order_id       -- Integer  
                - price_per_unit -- Float
                - quantity       -- Integer 
                - product        -- String(255)
                
        
    """
    __tablename__ = 'sales_orderitem'
    __table_args__ = (db.UniqueConstraint(
                    'product', 'order_id', 
                    name = 'unique_orderitem_order'),)
    
    serialize_only = ('id', 'price_per_unit', 'quantity', 'product', 'order','total_delivered', 'total_amount')
    serialize_rules = ('-deliveries.sales_orderitem','total_delivered', 'total_amount')
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, 
                    db.ForeignKey("sales_order.id", ondelete='RESTRICT'))
    price_per_unit = db.Column(db.Numeric(precision=10, scale=2), 
                             nullable=False, default=0.0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    product = db.Column(db.String(255), nullable=False)
    
    # Tracer fields
    created = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    updated = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    user_updated = db.Column(db.String(30),  default="Admin")
    
    # Relationships 
    
    # Populate relate to field Order.order_items
    order = db.relationship("Order", back_populates="order_items")
    
    # Populate relate to field Delivery.order_item
    deliveries = db.relationship(
                "Delivery", 
                # backref=db.backref("sales_orderitem", lazy="joined"),
                back_populates="order_item", 
                passive_deletes=True,
                lazy="select"
            )
    
    def delivered(self):
        from backend.apps.stocks.models.deliveries import Delivery
        delivered = 0
        for d in Delivery.query.filter(Delivery.order_item_id==self.id):
            delivered += int(d.delivered_quantity)
        
        return delivered
    
    def balance(self):
         # set by sistem
        return self.quantity - self.delivered()
    
    def total_delivered(self):
        return round(float(self.delivered() * float(self.price_per_unit)),2)
    
    def total_amount(self):
        return round(float(self.quantity) * float(self.price_per_unit), 2)

    def __init__(self, 
                 order_id, 
                 price_per_unit, 
                 quantity,
                 product):
        
        self.order_id = order_id
        self.price_per_unit = price_per_unit
        self.quantity = quantity
        self.product = product
        
    def __repr__(self):
        return '''<id:{}, order_id:{}, price_per_unit:{}, 
            quantity:{}, product:{}>'''.format(
            self.id, self.order_id, self.price_per_unit, 
            self.quantity, self.product)
    
    


