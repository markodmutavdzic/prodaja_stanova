from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app import enums, db
from app.marsh import new_apartment_schema, edit_apartment_schema, filter_apartment_schema
from app.models import Apartment
from app.serialize import apartments_serialize, apartment_serialize
from app.token import token_required

apa = Blueprint('apartment', __name__, url_prefix='/apartment')


@apa.route('/')
def hello():
    return 'Zdravo, apartment', 200


@apa.route('/add', methods=['POST'])
# @token_required
# def add_apartment(current_user):
def add_apartment():
#     if current_user.role is not enums.UserRole.ADMIN:
#         return jsonify({"message": "User must be ADMIN"}), 400

    try:
        data = new_apartment_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    new_apartment = Apartment()
    new_apartment.lamella = data.get('lamella')
    new_apartment.quadrature = data.get('quadrature')
    new_apartment.floor = data.get('floor')
    new_apartment.num_rooms = data.get('num_rooms')
    new_apartment.orientation = data.get('orientation')
    new_apartment.num_terrace = data.get('num_terrace')
    new_apartment.price = data.get('price')
    new_apartment.status = data.get('status')
    new_apartment.new_construction = data.get('new_construction')
    new_apartment.in_construction = data.get('in_construction')
    new_apartment.available_from = data.get('available_from')

    db.session.add(new_apartment)
    db.session.commit()

    return jsonify({"message": "New apartment created."}), 200


@apa.route('/edit', methods=['POST'])
@token_required
def edit_apartment(current_user):
    if current_user.role is not enums.UserRole.ADMIN:
        return jsonify({"message": "User must be ADMIN"}), 400

    try:
        data = edit_apartment_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartment = Apartment.query.filter(Apartment.id == data.get('id')).first()
    if not apartment:
        return jsonify({"message": "Apartment with that id doesnt exists."}), 400

    if data.get('lamella'):
        apartment.lamella = data.get('lamella')
    if data.get('quadrature'):
        apartment.quadrature = data.get('quadrature')
    if data.get('floor'):
        apartment.floor = data.get('floor')
    if data.get('num_rooms'):
        apartment.num_rooms = data.get('num_rooms')
    if data.get('orientation'):
        apartment.orientation = data.get('orientation')
    if data.get('num_terrace'):
        apartment.num_terrace = data.get('num_terrace')
    if data.get('price'):
        apartment.price = data.get('price')
    if data.get('status'):
        apartment.status = data.get('status')
    if data.get('new_construction'):
        apartment.new_construction = data.get('new_construction')
    if data.get('in_construction'):
        apartment.in_construction = data.get('in_construction')
    if data.get('available_from'):
        apartment.available_from = data.get('available_from')

    db.session.commit()

    return jsonify({"message": "Apartment edited."}), 200


@apa.route('/all', methods=['POST'])
# @token_required
def all_apartments():

    try:
        data = filter_apartment_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartments = Apartment.query

    if data:
        if data.get("quadrature_from"):
            apartments = apartments.filter(Apartment.quadrature > data.get("quadrature_from"))
        if data.get("quadrature_to"):
            apartments = apartments.filter(Apartment.quadrature < data.get("quadrature_to"))
        # if data.quadrature_to:
        #     apartments = apartments.filter(Apartment.quadrature < data.quadrature_to)






    apartments = apartments.all()

    result = apartments_serialize(apartments)

    return jsonify({"apartments": result}), 200
