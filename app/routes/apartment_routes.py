import os

from flask import Blueprint, jsonify, request, current_app
from marshmallow import ValidationError

from app import enums, db
from app.marsh import new_apartment_schema, edit_apartment_schema, filter_apartment_schema, delete_schema
from app.models import Apartment, Image
from app.serialize import apartments_serialize
from app.token import token_required

apa = Blueprint('apartment', __name__, url_prefix='/apartment')
UPLOAD_IMAGE_TYPES = [".jpg", ".jpeg", ".gif", ".png"]


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
    new_apartment.address = data.get('address')
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



@apa.route('/add_images', methods=['POST'])
def upload_image():
    images = request.files.getlist("images")
    apartment_id = int(request.form.get("id"))
    apartment = Apartment.query.filter(Apartment.id == apartment_id).first()
    if not apartment:
        return jsonify({"message": "Apartment with that id doesnt exists."}), 400

    if images:
        for image in images:

            filename = image.filename
            new_image = Image()
            new_image.file_name = image.filename
            new_image.location = "not yet"
            new_image.url = "not yet"
            db.session.add(new_image)
            db.session.flush()
            if filename != "":
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in UPLOAD_IMAGE_TYPES:
                    db.session.rollback()
                    return jsonify({"message": "Wrong image type"}), 400
                image.save(
                    os.path.join(
                        current_app.config.get("ROOT_DIR"),
                        "static/uploads",
                        "{}_{}".format(new_image.id, filename),
                    )
                )
            new_image.location = os.path.join(
                current_app.config.get("ROOT_DIR"),
                "static/uploads",
                "{}_{}".format(new_image.id, filename),
            )
            new_image.url = os.path.join("uploads", "{}_{}".format(new_image.id, filename))
            db.session.add(new_image)
            apartment.images.append(new_image)

        db.session.commit()

    return jsonify({"message": "Images uploaded"}), 200

@apa.route('/edit', methods=['POST'])
# @token_required
# def edit_apartment(current_user):
def edit_apartment():
#     if current_user.role is not enums.UserRole.ADMIN:
#         return jsonify({"message": "User must be ADMIN"}), 400

    try:
        data = edit_apartment_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartment = Apartment.query.filter(Apartment.id == data.get('id'))
    if not apartment:
        return jsonify({"message": "Apartment with that id doesnt exists."}), 400
    apartment.update(data)

    # if data.get('lamella'):
    #     apartment.lamella = data.get('lamella')
    # if data.get('address'):
    #     apartment.address = data.get('address')
    # if data.get('quadrature'):
    #     apartment.quadrature = data.get('quadrature')
    # if data.get('floor'):
    #     apartment.floor = data.get('floor')
    # if data.get('num_rooms'):
    #     apartment.num_rooms = data.get('num_rooms')
    # if data.get('orientation'):
    #     apartment.orientation = data.get('orientation')
    # if data.get('num_terrace'):
    #     apartment.num_terrace = data.get('num_terrace')
    # if data.get('price'):
    #     apartment.price = data.get('price')
    # if data.get('status'):
    #     apartment.status = data.get('status')
    # if data.get('new_construction'):
    #     apartment.new_construction = data.get('new_construction')
    # if data.get('in_construction'):
    #     apartment.in_construction = data.get('in_construction')
    # if data.get('available_from'):
    #     apartment.available_from = data.get('available_from')

    db.session.commit()

    return jsonify({"message": "Apartment edited."}), 200


@apa.route('/all', methods=['POST'])
def all_apartments():

    try:
        data = filter_apartment_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartments = Apartment.query

    if data:
        if data.get("lamella"):
            apartments = apartments.filter(Apartment.lamella.ilike("%"+data.get("lamella")+"%"))
        if data.get("address"):
            apartments = apartments.filter(Apartment.address.ilike("%"+data.get("address")+"%"))
        if data.get("quadrature_from"):
            apartments = apartments.filter(Apartment.quadrature >= data.get("quadrature_from"))
        if data.get("quadrature_to"):
            apartments = apartments.filter(Apartment.quadrature <= data.get("quadrature_to"))
        if data.get("floor_from"):
            apartments = apartments.filter(Apartment.floor >= data.get("floor_from"))
        if data.get("floor_to"):
            apartments = apartments.filter(Apartment.floor <= data.get("floor_to"))
        if data.get("num_rooms_from"):
            apartments = apartments.filter(Apartment.num_rooms >= data.get("num_rooms_from"))
        if data.get("num_rooms_to"):
            apartments = apartments.filter(Apartment.num_rooms <= data.get("num_rooms_to"))
        if data.get("orientation"):
            apartments = apartments.filter(Apartment.orientation == data.get("orientation"))
        if data.get("num_terrace_from"):
            apartments = apartments.filter(Apartment.num_terrace >= data.get("num_terrace_from"))
        if data.get("num_terrace_to"):
            apartments = apartments.filter(Apartment.num_terrace <= data.get("num_terrace_to"))
        if data.get("price_from"):
            apartments = apartments.filter(Apartment.price >= data.get("price_from"))
        if data.get("price_to"):
            apartments = apartments.filter(Apartment.price <= data.get("price_to"))
        if data.get("status"):
            apartments = apartments.filter(Apartment.status == data.get("status"))
        if data.get("new_construction"):
            apartments = apartments.filter(Apartment.new_construction.is_(data.get("new_construction")))
        if data.get("in_construction"):
            apartments = apartments.filter(Apartment.in_construction.is_(data.get("in_construction")))
        if data.get("available_from_from"):
            apartments = apartments.filter(Apartment.available_from >= data.get("available_from_from"))
        if data.get("available_from_to"):
            apartments = apartments.filter(Apartment.available_from <= data.get("available_from_to"))
        if data.get("order_id"):
            if data.get("order_id") == enums.Order.ASC:
                apartments = apartments.order_by(Apartment.id.asc())
            if data.get("order_id") == enums.Order.DESC:
                apartments = apartments.order_by(Apartment.id.desc())
        if data.get("order_price"):
            if data.get("order_price") == enums.Order.ASC:
                apartments = apartments.order_by(Apartment.price.asc())
            if data.get("order_price") == enums.Order.DESC:
                apartments = apartments.order_by(Apartment.price.desc())

    apartments = apartments.all()

    result = apartments_serialize(apartments)

    return jsonify({"apartments": result}), 200


@apa.route("/delete", methods=['POST'])
def delete_apartment():
    try:
        data = delete_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartment_for_delete = Apartment.query.filter(Apartment.id == data.get("id")).first()
    if not apartment_for_delete:
        return jsonify({"message": "Apartment with that id doesnt exists."}), 400

    db.session.delete(apartment_for_delete)
    db.session.commit()

    return jsonify({"message": "Apartment deleted"}), 200
