from __future__ import unicode_literals, absolute_import

# Password --------------------------------------------------------------------
# https://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy
# https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem

import logging

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin

from backend.run import db

# from backend.apps.masters.models.companies import Company

from backend.logs import FILE_HANDLER

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)


class Customer(db.Model, SerializerMixin):
    """
        Models    : Customer
        Table     : masters_customer
        Fields    :
                - user_id    -- String(80)
                - name       -- String(255)
                - username   -- String(80)
                - password   -- Text
                - company_id -- Integer
                - credit_cards -- String(50)
        
    """
    __tablename__ = 'masters_customer'
    __table_args__ = (db.UniqueConstraint(
                    'user_id', 'company_id', 
                    name = 'unique_customer_company'),)
    
    serialize_only = ('user_id','name','username', 'company', 'credit_cards')
    serialize_rules = ('-orders.masters_customer',)
    
    user_id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=True)
    
    company_id = db.Column(db.Integer, 
                    db.ForeignKey("masters_company.id", ondelete='RESTRICT'))
    
    credit_cards = db.Column(db.String(80), nullable=True)
    
    # Tracer fields
    created = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    updated = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    user_updated = db.Column(db.String(30),  default="Admin")
    
    # Relationships 
    
    # Populate relate to field Company.customers
    company = db.relationship("Company", back_populates="customers")
    
    # Populate relate to field Order.customer
    orders = db.relationship(
                "Order", 
                # backref=db.backref("masters_customer", lazy="joined"),
                back_populates="customer",
                lazy="select"
            )
    
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            print("{} is {}".format(key,value))
        
        super(Customer, self).__init__(*args, **kwargs)
        
    def __init__(self, 
                 user_id, 
                 name, 
                 username,  
                 company_id, 
                 credit_cards):
        
        self.user_id = user_id
        self.name = name
        self.username = username
        self.company_id = company_id
        self.credit_cards = credit_cards

    def __repr__(self):
        return '<user_id: {}, username:{} company_id:{}>'.format(
            self.user_id, self.username, self.company_id)
    
    def set_password(self, password):
        self.password = generate_password_hash(str(password))

    def check_password(self, password):
        return check_password_hash(self.password, str(password))
    
    
    
    
    