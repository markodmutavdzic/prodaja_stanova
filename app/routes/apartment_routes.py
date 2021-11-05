from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app import enums, db
from app.marsh import new_apartment_schema
from app.models import Apartment
from app.token import token_required

apa = Blueprint('apartment', __name__, url_prefix='/apartment')


@apa.route('/')
def hello():
    return 'Zdravo, apartment', 200


@apa.route('/add')
@token_required
def add_apartment(current_user):
    if current_user.role is not enums.UserRole.ADMIN:
        return jsonify({"message": "User must be ADMIN"}), 400

    try:
        data = new_apartment_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    new_apartment = Apartment()
    new_apartment.lamella = data.get('lamella')
    new_apartment.quadrature = data.get('quadrature')
    new_apartment.floor = data.get('floor')
    new_apartment.num_rooms = data.num_rooms
    new_apartment.orientation = data.orientation
    new_apartment.num_terrace = data.num_terrace
    new_apartment.price = data.price
    new_apartment.status = data.status
    new_apartment.new_construction = data.new_construction
    new_apartment.in_construction = data.in_construction
    new_apartment.available_from = data.available_from

    db.session.add(new_apartment)
    db.session.commit()

    return jsonify({"message": "New apartment created."}), 200