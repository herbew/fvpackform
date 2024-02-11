from __future__ import unicode_literals, absolute_import

# ER --------------------------------------------------------------------------
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
# https://github.com/w8s/flask-model-relationships

import logging

from datetime import datetime
from backend.run import db

from sqlalchemy_serializer import SerializerMixin

from backend.logs import FILE_HANDLER

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__file__)
file_handler = FILE_HANDLER
log.addHandler(file_handler)

class Company(db.Model, SerializerMixin):
    """
        Models    : Company
        Table     : masters_company
        Fields    :
                - id     -- Integer
                - name   -- String
        
    """
    __tablename__ = 'masters_company'
    
    serialize_only = ('id','name')
    serialize_rules = ('-customers.masters_company',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    
    # Tracer fields
    created = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    user_updated = db.Column(db.String(30),  default="Admin")
    
    # Relationships
    
    # Populate relate to field Customer.company.
    customers = db.relationship(
                "Customer", 
                # backref=db.backref("masters_company", lazy="joined"), 
                back_populates="company", 
                passive_deletes=True,
                lazy="select"
            )
    

    def __init__(self, 
                 name):
        self.name = name

    def __repr__(self):
        return '<id: {}, name:{} >'.format(self.id, self.name)