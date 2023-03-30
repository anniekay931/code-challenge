#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Sweet, Vendor, VendorSweet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/vendors', methods = ['GET'])
def vendors():
    vendors = Vendor.query.all()
    vendors_dict = [vendor.to_dict() for vendor in vendors]

    response = make_response(
        jsonify(vendors_dict),
        200
    )

    return response

@app.route('/vendors/<int:id>', methods = ['GET'])
def vendorByID(id):
    vendor = Vendor.query.filter_by(id =id).first()

    if vendor:

        vendor_dict = vendor.to_dict()

        response = make_response(
            jsonify(vendor_dict),
            200
        )

    else:

        response = make_response(
            {"error": "Vendor not found"},
            404
        )

    return response

@app.route('/sweets', methods = ['GET'])
def sweets():
    sweets = Sweet.query.all()
    sweets_dict = [sweet.to_dict() for sweet in sweets]

    response = make_response(
        jsonify(sweets_dict),
        200
    )

    return response

@app.route('/sweets/<int:id>', methods = ['GET'])
def sweetByID(id):
    sweet = Sweet.query.filter_by(id = id).first()

    if sweet:

        sweet_dict = sweet.to_dict()

        response = make_response(
            jsonify(sweet_dict),
            200
        )

    else:

        response = make_response(
            {"error": "Sweet not found"},
            404
        )
    
    return response

@app.route('/vendor_sweets', methods = ['POST'])
def vendorSweets():
    try:

        new_vendor_sweet = VendorSweet(
            price = request.get_json()['price'],
            vendor_id = request.get_json()['vendor_id'],
            sweet_id = request.get_json()['sweet_id']
        )

        db.session.add(new_vendor_sweet)
        db.session.commit()

        vendor_sweet_dict = new_vendor_sweet.to_dict()

        response = make_response(
            jsonify(vendor_sweet_dict),
            201
        )

    except ValueError:

        response = make_response(
            {"error": "Validation errors"},
            400
        )

    return response 

@app.route('/vendor_sweets/<int:id>', methods = ['DELETE'])
def delete_vendor_sweet(id):
    vendor_sweet = VendorSweet.query.filter_by(id =id).first()

    if vendor_sweet:

        db.session.delete(vendor_sweet)
        db.session.commit()

        response = make_response(
            {},
            200
        )

    else:

        response = make_response(
            {"error": "VendorSweet not found"},
            404
        )
    
    return response







    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
