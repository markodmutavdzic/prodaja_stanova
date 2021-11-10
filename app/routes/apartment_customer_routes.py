from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app import enums
from app.marsh import new_apartment_customer_schema, edit_apartment_customer_schema, customers_for_apartment_schema, \
    apartment_for_customer_schema, delete_schema, edit_apartment_customer_for_sale_schema
from app.models import ApartmentCustomer, db, Customer, Apartment
from app.serialize import customer_apartment_serialize, apartment_customer_serialize
from app.token import token_required

apc = Blueprint('apartment_customer', __name__, url_prefix='/apartment_customer')


@apc.route("/")
def hello():
    return 'Zdravo, apartment_customer', 200


# TODO logika za price approved
@apc.route("/add", methods=['POST'])
def add_apartment_customer():
    try:
        data = new_apartment_customer_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    offer_exists = ApartmentCustomer.query.filter(ApartmentCustomer.apartment_id == data.get("apartment_id"),
                                                  ApartmentCustomer.customer_id == data.get("customer_id")).first()
    if offer_exists:
        return jsonify({"message": "Offer from that costumer for that apartment already exists"}), 200

    apartment = Apartment.query.filter(Apartment.id == data.get("apartment_id")).first()
    new_apartment_customer = ApartmentCustomer()
    new_apartment_customer.apartment_id = data.get("apartment_id")
    new_apartment_customer.customer_id = data.get("customer_id")
    new_apartment_customer.customer_status = data.get("customer_status")
    new_apartment_customer.note = data.get("note")
    new_apartment_customer.currency = data.get("currency")
    new_apartment_customer.payment_method = data.get("payment_method")
    new_apartment_customer.deposit_amount = data.get("deposit_amount")
    new_apartment_customer.contract_deadline = data.get("contract_deadline")
    new_apartment_customer.bank = data.get("bank")
    new_apartment_customer.loan_amount = data.get("loan_amount")
    new_apartment_customer.cash_amount = data.get("cash_amount")
    new_apartment_customer.contract_number = data.get("contract_number")
    new_apartment_customer.contract_date = data.get("contract_date")
    new_apartment_customer.customer_price = data.get("customer_price")
    if new_apartment_customer.customer_price < apartment.lowest_price:
        new_apartment_customer.price_approved = False
    else:
        new_apartment_customer.price_approved = True

    db.session.add(new_apartment_customer)
    db.session.commit()

    return jsonify({"message": "New offer created"}), 200


# TODO logika za price approved
# @token_required
@apc.route("/edit", methods=['POST'])
def edit_apartment_customer():
# def edit_apartment_customer(current_user):
#     if current_user.role is not enums.UserRole.FINANSIJE:
    # return jsonify({"message": "User must be FINANSIJE"}), 400
    try:
        data = edit_apartment_customer_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartment_customer = ApartmentCustomer.query.filter(ApartmentCustomer.id == data.get('id')).first()
    if not apartment_customer:
        return jsonify({"message": "Offer with that id doesnt exists"}), 400
    # apartment_customer.update(data)
    #
    # db.session.commit()

    apartment = Apartment.query.filter(Apartment.id == apartment_customer.apartment_id).first()
    if data.get("apartment_id"):
        apartment_customer.apartment_id = data.get("apartment_id")
    if data.get("customer_id"):
        apartment_customer.customer_id =  data.get("customer_id")
    if data.get("customer_status"):
        apartment_customer.customer_status = data.get("customer_status")
    if data.get("note"):
        apartment_customer.note = data.get("note")
    if data.get("currency"):
        apartment_customer.currency = data.get("currency")
    if data.get("payment_method"):
        apartment_customer.payment_method = data.get("payment_method")
    if data.get("deposit_amount"):
        apartment_customer.deposit_amount = data.get("deposit_amount")
    if data.get("contract_deadline"):
        apartment_customer.contract_deadline = data.get("contract_deadline")
    if data.get("bank"):
        apartment_customer.bank = data.get("bank")
    if data.get("loan_amount"):
        apartment_customer.loan_amount = data.get("loan_amount")
    if data.get("cash_amount"):
        apartment_customer.cash_amount = data.get("cash_amount")
    if data.get("contract_number"):
        apartment_customer.contract_number = data.get("contract_number")
    if data.get("contract_date"):
        apartment_customer.contract_date = data.get("contract_date")
    if data.get("customer_price"):
        apartment_customer.customer_price = data.get("customer_price")
    if data.get("currency"):
        if apartment_customer.customer_price < apartment.lowest_price:
            apartment_customer.price_approved = False
        else:
            apartment_customer.price_approved = True

    db.session.commit()

    return jsonify({"message": "Offer edited"}), 200


@apc.route("/edit_for_sale", methods=['POST'])
def edit_apartment_customer_for_sale():
    try:
        data = edit_apartment_customer_for_sale_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartment_customer = ApartmentCustomer.query.filter(ApartmentCustomer.id == data.get('id'))
    if not apartment_customer:
        return jsonify({"message": "Offer with that id doesnt exists"}), 400
    apartment_customer.update(data)

    db.session.commit()

    return jsonify({"message": "Offer edited"}), 200


@apc.route("/customers_for_apartment", methods=['POST'])
def customers_for_apartment():
    try:
        data = customers_for_apartment_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    customers_apartments = db.session.query(Customer, ApartmentCustomer)\
        .join(ApartmentCustomer, ApartmentCustomer.customer_id == Customer.id).\
        filter(ApartmentCustomer.apartment_id == data.get("apartment_id")).all()

    result = customer_apartment_serialize(customers_apartments)

    return jsonify({"customers_for_apartment": result}), 200


@apc.route("/apartment_for_customer", methods=['POST'])
def apartment_for_customer():
    try:
        data = apartment_for_customer_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartments_customer = db.session.query(Apartment, ApartmentCustomer)\
        .join(ApartmentCustomer, ApartmentCustomer.apartment_id == Apartment.id).\
        filter(ApartmentCustomer.customer_id == data.get("customer_id")).all()

    result = apartment_customer_serialize(apartments_customer)

    return jsonify({"apartments_for_customer": result}), 200


@apc.route("/delete", methods=['POST'])
def delete_apartment_customer():
    try:
        data = delete_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartment_customer_for_delete = ApartmentCustomer.query.filter(ApartmentCustomer.id == data.get("id")).first()
    if not apartment_customer_for_delete:
        return jsonify({"message": "Offer with that id doesnt exists."}), 400

    db.session.delete(apartment_customer_for_delete)
    db.session.commit()

    return jsonify({"message": "Offer deleted"}), 200

