from __future__ import unicode_literals, absolute_import

import logging, pytz
from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from backend.run import db, os

from backend.logs import FILE_HANDLER

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)


class Order(db.Model, SerializerMixin):
    """
        Models    : Order
        Table     : sales_order
        Fields    :
                - id         -- Integer
                - created_at -- DateTime
                - order_name -- String(255)
                - customer_id-- String(80)
        
    """
    __tablename__ = 'sales_order'
    __table_args__ = (db.UniqueConstraint(
                    'order_name', 'customer_id', 
                    name = 'unique_order_customer'),)
    
    serialize_only = ('id', 'created_at_local', 'created_at_local_str', 'order_name', 'customer')
    serialize_rules = ('-order_items.sales_order',)
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    order_name = db.Column(db.String(255), nullable=False, unique=True)
    
    customer_id = db.Column(db.String(80), 
                    db.ForeignKey("masters_customer.user_id", ondelete='RESTRICT'))
    
    # Tracer fields
    created = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    updated = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    user_updated = db.Column(db.String(30),  default="Admin")
    
    # Relationships 
    
    # Populate relate to field Customer.orders
    customer = db.relationship("Customer", back_populates="orders")
    
    # Populate relate to field OrderItem.order
    order_items = db.relationship(
                "OrderItem", 
                #backref=db.backref("sales_order", lazy="joined"),
                back_populates="order", 
                passive_deletes=True,
                lazy="select"
            )
    
    def __init__(self, 
                 created_at, 
                 order_name, 
                 customer_id):
        
        self.created_at = created_at
        self.order_name = order_name
        self.customer_id = customer_id

    def __repr__(self):
        return '<id: {}, order_name:{} customer_id:{} created_at :{}>'.format(
            self.id, self.order_name, self.customer_id, self.created_at)
    
    @property
    def created_at_local(self):
        import pytz
        local_string = self.created_at.astimezone(
            pytz.timezone(os.environ['TZ'])).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        local_datetime = datetime.strptime(local_string,'%Y-%m-%d %H:%M:%S %Z%z')
        return local_datetime
    
    @property
    def created_at_local_str(self):
        def ordinal(n: int) -> str:
            """
                derive the ordinal numeral for a given number n
            """
            return f"{n:d}{'tsnrhtdd'[(n//10%10!=1)*(n%10<4)*n%10::4]}"
        
        dayo = ordinal(self.created_at_local.day)
        
        dts = datetime.strftime(
            self.created_at_local,f"%Y %b {dayo}, %I:%M %p")
        
        
        return "{} {}".format(dts, self.created_at_local.tzname())

        

