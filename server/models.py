from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Vendor(db.Model, SerializerMixin):
    __tablename__ = "vendors"

    serialize_rules = ('-sweets.vendors', '-vendor_sweets.vendor')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    vendor_sweets = db.relationship('VendorSweet', backref = 'vendor')

class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    serialize_rules = ('-vendor_sweets.sweet', '-vendors.sweet')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    vendor_sweets = db.relationship('VendorSweet', backref = 'sweet')

class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    serialize_rules = ('-sweet.vendor_sweets', '-vendor.vendor_sweets')
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('price')
    def validates_price(self, key, price):
        if not price or price < 0:
            raise ValueError('Must have a price above 0')
        return price

# Add models here

# for relationships between tables, name these "vendor_sweets"