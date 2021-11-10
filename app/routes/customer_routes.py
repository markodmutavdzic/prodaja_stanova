from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.marsh import new_customer_schema, edit_customer_schema, search_customer_schema, delete_schema
from app.models import Customer, db
from app.serialize import customers_serialize

cus = Blueprint('customer', __name__, url_prefix='/customer')


@cus.route('/')
def hello():
    return 'Zdravo, customer', 200


@cus.route('/add', methods=['POST'])
def add_customer():

    try:
        data = new_customer_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    new_customer = Customer()
    new_customer.legal_entity = data.get("legal_entity")
    new_customer.name = data.get("name")
    new_customer.email = data.get("email")
    new_customer.telephone_number = data.get("telephone_number")
    new_customer.pib_jmbg = data.get("pib_jmbg")
    new_customer.place = data.get("place")
    new_customer.street = data.get("street")
    new_customer.num = data.get("num")
    new_customer.date_of_first_visit = data.get("date_of_first_visit")

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "New customer created."}), 200


@cus.route('/edit', methods=['POST'])
def edit_customer():

    try:
        data = edit_customer_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    customer = Customer.query.filter(Customer.id == data.get('id')).first()
    if not customer:
        return jsonify({"message": "Customer with that id doesnt exists."}), 400

    if data.get('legal_entity'):
        customer.legal_entity = data.get('legal_entity')
    if data.get('name'):
        customer.name = data.get('name')
    if data.get('email'):
        customer.email = data.get('email')
    if data.get('telephone_number'):
        customer.telephone_number = data.get('telephone_number')
    if data.get('pib_jmbg'):
        customer.pib_jmbg = data.get('pib_jmbg')
    if data.get('place'):
        customer.place = data.get('place')
    if data.get('street'):
        customer.street = data.get('street')
    if data.get('num'):
        customer.num = data.get('num')
    if data.get('date_of_first_visit'):
        customer.date_of_first_visit = data.get('date_of_first_visit')

    db.session.commit()

    return jsonify({"message": "Customer edited."}), 200


@cus.route('/all', methods=['POST'])
def all_customer():
    try:
        data = search_customer_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    customers = Customer.query

    if data:
        if data.get('legal_entity'):
            customers = customers.filter(Customer.legal_entity.ilike("%"+data.get("legal_entity")+"%"))
        if data.get('name'):
            customers = customers.filter(Customer.name.ilike("%" + data.get("name") + "%"))
        if data.get('email'):
            customers = customers.filter(Customer.email.ilike("%" + data.get("email") + "%"))
        if data.get('telephone_number'):
            customers = customers.filter(Customer.telephone_number.ilike("%" + data.get("telephone_number") + "%"))
        if data.get('pib_jmbg'):
            customers = customers.filter(Customer.pib_jmbg.ilike("%" + data.get("pib_jmbg") + "%"))
        if data.get('place'):
            customers = customers.filter(Customer.place.ilike("%" + data.get("place") + "%"))
        if data.get('street'):
            customers = customers.filter(Customer.street.ilike("%" + data.get("street") + "%"))
        if data.get('num'):
            customers = customers.filter(Customer.num.ilike("%" + data.get("num") + "%"))
        if data.get('date_of_first_visit_from'):
            customers = customers.filter(Customer.date_of_first_visit >= data.get('date_of_first_visit_from'))
        if data.get('date_of_first_visit_to'):
            customers = customers.filter(Customer.date_of_first_visit <= data.get('date_of_first_visit_to'))

    customers = customers.all()

    result = customers_serialize(customers)

    return jsonify({"customers": result}), 200


@cus.route("/delete", methods=['POST'])
def delete_customer():
    try:
        data = delete_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    customer_for_delete = Customer.query.filter(Customer.id == data.get("id")).first()
    if not customer_for_delete:
        return jsonify({"message": "Customer with that id doesnt exists."}), 400

    db.session.delete(customer_for_delete)
    db.session.commit()

    return jsonify({"message": "Customer deleted"}), 200
