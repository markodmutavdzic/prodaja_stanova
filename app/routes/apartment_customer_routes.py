from datetime import datetime, date

from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from docxtpl import DocxTemplate
from app import enums
from app.marsh import new_apartment_customer_schema, edit_apartment_customer_schema, \
    edit_apartment_customer_for_sale_schema, price_approved_schema, id_schema, price_approval_schema
from app.models import ApartmentCustomer, db, Customer, Apartment
from app.serialize import customer_apartment_serialize, apartment_customer_serialize, price_for_approval_serialize, \
    apartment_serialize, customer_serialize
from app.token import token_required
from num2words import num2words
import requests

apc = Blueprint('apartment_customer', __name__, url_prefix='/apartment_customer')


@apc.route('/')
def hello():
    return 'Zdravo, apartment_customer', 200


@apc.route('/add', methods=['POST'])
def add_apartment_customer():
    try:
        data = new_apartment_customer_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    offer_exists = ApartmentCustomer.query.filter(ApartmentCustomer.apartment_id == data.get('apartment_id'),
                                                  ApartmentCustomer.customer_id == data.get('customer_id')).first()
    if offer_exists:
        return jsonify({'message': 'Offer from that costumer for that apartment already exists'}), 400

    apartment = Apartment.query.filter(Apartment.id == data.get('apartment_id')).first()
    if not apartment:
        return jsonify({'message': 'Apartment with that id doesnt exist'}), 400
    if apartment.status == enums.Status.PRODAT:
        return jsonify({'message': 'Apartment is already sold'}), 400

    new_apartment_customer = ApartmentCustomer()
    new_apartment_customer.apartment_id = data.get('apartment_id')
    new_apartment_customer.customer_id = data.get('customer_id')
    new_apartment_customer.customer_status = data.get('customer_status')
    new_apartment_customer.note = data.get('note')
    new_apartment_customer.currency = data.get('currency')
    new_apartment_customer.payment_method = data.get('payment_method')
    new_apartment_customer.deposit_amount = data.get('deposit_amount')
    new_apartment_customer.contract_deadline = data.get('contract_deadline')
    new_apartment_customer.bank = data.get('bank')
    new_apartment_customer.loan_amount = data.get('loan_amount')
    new_apartment_customer.cash_amount = data.get('cash_amount')
    new_apartment_customer.contract_number = data.get('contract_number')
    new_apartment_customer.contract_date = data.get('contract_date')
    new_apartment_customer.customer_price = data.get('customer_price')
    if new_apartment_customer.customer_price >= apartment.lowest_price:
        new_apartment_customer.price_approved = True
    else:
        new_apartment_customer.price_approved = None

    if new_apartment_customer.customer_status == enums.CostumerStatus.REZERVISAO:
        apartment.status = enums.Status.REZERVISAN
        apartment.date_reserved = date.today()
    elif new_apartment_customer.customer_status == enums.CostumerStatus.KUPIO:
        if new_apartment_customer.price_approved is True:
            apartment.status = enums.Status.PRODAT
            apartment.date_sold = date.today()
        elif new_apartment_customer.price_approved is not True:
            return jsonify({'message': 'Price must be approved'})

    db.session.add(new_apartment_customer)
    db.session.commit()

    return jsonify({'message': 'New offer created'}), 200


@apc.route('/edit', methods=['POST'])
# @token_required
def edit_apartment_customer():
    # def edit_apartment_customer(current_user):
    #     if current_user.role is not enums.UserRole.FINANSIJE:
    # return jsonify({'message': 'User must be FINANSIJE'}), 400
    try:
        data = edit_apartment_customer_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartment_customer = ApartmentCustomer.query.filter(ApartmentCustomer.id == data.get('id')).first()
    if not apartment_customer:
        return jsonify({'message': 'Offer with that id doesnt exists'}), 400

    apartment = Apartment.query.filter(Apartment.id == apartment_customer.apartment_id).first()
    if not apartment:
        return jsonify({'message': 'Apartment with that id doesnt exist'}), 400
    if apartment.status == enums.Status.PRODAT:
        return jsonify({'message': 'Apartment is already sold'}), 400

    if data.get('apartment_id'):
        apartment_customer.apartment_id = data.get('apartment_id')
    if data.get('customer_id'):
        apartment_customer.customer_id = data.get('customer_id')
    if data.get('customer_status'):
        apartment_customer.customer_status = data.get('customer_status')
        if apartment_customer.customer_status == enums.CostumerStatus.REZERVISAO:
            apartment.status = enums.Status.REZERVISAN
            apartment.date_reserved = date.today()
        elif apartment_customer.customer_status == enums.CostumerStatus.KUPIO:
            if apartment_customer.price_approved is True:
                apartment.status = enums.Status.PRODAT
                apartment.date_sold = date.today()
            elif apartment_customer.price_approved is not True:
                return jsonify({'message': 'Price must be approved'})
    if data.get('note'):
        apartment_customer.note = data.get('note')
    if data.get('currency'):
        apartment_customer.currency = data.get('currency')
    if data.get('payment_method'):
        apartment_customer.payment_method = data.get('payment_method')
    if data.get('deposit_amount'):
        apartment_customer.deposit_amount = data.get('deposit_amount')
    if data.get('contract_deadline'):
        apartment_customer.contract_deadline = data.get('contract_deadline')
    if data.get('bank'):
        apartment_customer.bank = data.get('bank')
    if data.get('loan_amount'):
        apartment_customer.loan_amount = data.get('loan_amount')
    if data.get('cash_amount'):
        apartment_customer.cash_amount = data.get('cash_amount')
    if data.get('contract_number'):
        apartment_customer.contract_number = data.get('contract_number')
    if data.get('contract_date'):
        apartment_customer.contract_date = data.get('contract_date')
    if data.get('customer_price'):
        apartment_customer.customer_price = data.get('customer_price')
        if apartment_customer.customer_price >= apartment.lowest_price:
            apartment_customer.price_approved = True
        else:
            apartment_customer.price_approved = None

    db.session.commit()

    return jsonify({'message': 'Offer edited'}), 200


@apc.route('/edit_for_sale', methods=['POST'])
def edit_apartment_customer_for_sale():
    try:
        data = edit_apartment_customer_for_sale_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartment_customer = ApartmentCustomer.query.filter(ApartmentCustomer.id == data.get('id')).first()
    if not apartment_customer:
        return jsonify({'message': 'Offer with that id doesnt exists'}), 400

    apartment = Apartment.query.filter(Apartment.id == apartment_customer.apartment_id).first()
    if not apartment:
        return jsonify({'message': 'Apartment with that id doesnt exist'}), 400
    if apartment.status == enums.Status.PRODAT:
        return jsonify({'message': 'Apartment is already sold'}), 400

    if data.get('customer_price'):
        apartment_customer.customer_price = data.get('customer_price')
        if apartment_customer.customer_price >= apartment.lowest_price:
            apartment_customer.price_approved = True
        else:
            apartment_customer.price_approved = None
    if data.get('customer_status'):
        apartment_customer.customer_status = data.get('customer_status')
        if apartment_customer.customer_status == enums.CostumerStatus.REZERVISAO:
            apartment.status = enums.Status.REZERVISAN
            apartment.date_reserved = date.today()
        elif apartment_customer.customer_status == enums.CostumerStatus.KUPIO:
            if apartment_customer.price_approved is True:
                apartment.status = enums.Status.PRODAT
                apartment.date_sold = date.today()
            elif apartment_customer.price_approved is not True:
                return jsonify({'message': 'Price must be approved'})
    if data.get('note'):
        apartment_customer.note = data.get('note')
    if data.get('currency'):
        apartment_customer.currency = data.get('currency')

    db.session.commit()

    return jsonify({'message': 'Offer edited'}), 200


@apc.route('/customers_for_apartment', methods=['POST'])
def customers_for_apartment():
    try:
        data = id_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    customers_apartments = db.session.query(Customer, ApartmentCustomer) \
        .join(ApartmentCustomer, ApartmentCustomer.customer_id == Customer.id). \
        filter(ApartmentCustomer.apartment_id == data.get('id'))\
        .paginate(per_page=2, page=data.get('page_num'), error_out=True)

    apartment_db = Apartment.query.filter(Apartment.id == data.get('id')).first()
    if not apartment_db:
        return jsonify({'message': 'Apartment with that id doesnt exist'}), 400
    apartment = apartment_serialize(apartment_db)
    result = customer_apartment_serialize(customers_apartments.items)

    return jsonify({"current page": customers_apartments.page,
                    "next_page": customers_apartments.next_num,
                    "perv_page": customers_apartments.prev_num},
                   {'apartment': apartment},
                   {'customers_for_apartment': result}), 200


@apc.route('/apartment_for_customer', methods=['POST'])
def apartment_for_customer():
    try:
        data = id_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartments_customer = db.session.query(Apartment, ApartmentCustomer) \
        .join(ApartmentCustomer, ApartmentCustomer.apartment_id == Apartment.id). \
        filter(ApartmentCustomer.customer_id == data.get('id'))\
        .paginate(per_page=2, page=data.get('page_num'), error_out=True)

    customer_db = Customer.query.filter(Customer.id == data.get('id')).first()
    if not customer_db:
        return jsonify({'message': 'Cutomer with that id doesnt exist'}), 400

    customer = customer_serialize(customer_db)
    result = apartment_customer_serialize(apartments_customer.items)

    return jsonify({"current page": apartments_customer.page,
                    "next_page": apartments_customer.next_num,
                    "perv_page": apartments_customer.prev_num},
                   {'customer': customer},
                   {'apartments_for_customer': result}), 200


@apc.route('/delete', methods=['POST'])
def delete_apartment_customer():
    try:
        data = id_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    apartment_customer_for_delete = ApartmentCustomer.query.filter(ApartmentCustomer.id == data.get('id')).first()
    if not apartment_customer_for_delete:
        return jsonify({'message': 'Offer with that id doesnt exists.'}), 400

    db.session.delete(apartment_customer_for_delete)
    db.session.commit()

    return jsonify({'message': 'Offer deleted'}), 200


@apc.route('/price_for_approval')
# @token_required
def price_for_approval():
    # def price_for_approval(current_user):
    #     if current_user.role is not enums.UserRole.FINANSIJE:
    # return jsonify({'message': 'User must be FINANSIJE'}), 400

    try:
        data = price_approval_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    customers_apartments_price = db.session.query(Apartment, Customer, ApartmentCustomer) \
        .join(Apartment, Apartment.id == ApartmentCustomer.apartment_id) \
        .join(Customer, Customer.id == ApartmentCustomer.customer_id) \
        .filter(ApartmentCustomer.price_approved.is_(None)) \
        .with_entities(ApartmentCustomer.id.label('offer_id'),
                       Apartment.id.label('apartment_id'),
                       Apartment.address.label('apartment_address'),
                       Apartment.quadrature.label('apartment_quadrature'),
                       Apartment.price.label('apartment_price'),
                       Apartment.lowest_price.label('apartment_lowest_price'),
                       ApartmentCustomer.price_approved.label('price_approved'),
                       ApartmentCustomer.customer_price.label('apartment_customer_price'),
                       Customer.id.label('customer_id'),
                       Customer.name.label('customer_name')
                       ).paginate(per_page=2, page=data.get('page_num'), error_out=True)

    result = price_for_approval_serialize(customers_apartments_price.items)

    return jsonify({"current page": customers_apartments_price.page,
                    "next_page": customers_apartments_price.next_num,
                    "perv_page": customers_apartments_price.prev_num},
                   {'price_for_approval': result}), 200


@apc.route('/price_approved', methods=['POST'])
# @token_required
def price_approved():
    # def price_for_approval(current_user):
    #     if current_user.role is not enums.UserRole.FINANSIJE:
    # return jsonify({'message': 'User must be FINANSIJE'}), 400

    try:
        data = price_approved_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    offer_for_approval = ApartmentCustomer.query.filter(ApartmentCustomer.id == data.get('id')).first()
    if not offer_for_approval:
        return jsonify({'message': 'Offer with that id doesnt exists.'}), 400
    offer_for_approval.price_approved = data.get('price_approved')
    db.session.commit()

    return jsonify({'message': 'Price approved'}), 200


@apc.route('/generate_contract', methods=['POST'])
# @token_required
def generate_contract():
    # def generate_contract(current_user):
    # if current_user.role is not enums.UserRole.FINANSIJE:
    # return jsonify({'message': 'User must be FINANSIJE'}), 400

    try:
        data = id_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    contract_data = db.session.query(Apartment, Customer, ApartmentCustomer) \
        .join(Apartment, Apartment.id == ApartmentCustomer.apartment_id) \
        .join(Customer, Customer.id == ApartmentCustomer.customer_id) \
        .filter(ApartmentCustomer.id == data.get('id')) \
        .with_entities(ApartmentCustomer.contract_number.label('contract_number'),
                       ApartmentCustomer.contract_date.label('contract_date'),
                       ApartmentCustomer.customer_price.label('price'),
                       ApartmentCustomer.currency.label('currency'),
                       Customer.name.label('name'),
                       Customer.place.label('place'),
                       Customer.street.label('street'),
                       Customer.num.label('num'),
                       Apartment.address.label('address'),
                       Apartment.quadrature.label('quadrature')
                       ).first()

    for data in contract_data:
        if data is None:
            return jsonify({'message': 'Please fill all necessary data'}), 400

    if contract_data.currency == enums.Currency.EUR:
        response = requests.get('https://kurs.resenje.org/api/v1/currencies/eur/rates/today')
        exchange_rate = response.json().get('exchange_middle')
        price_rsd = float(contract_data.price) * exchange_rate
    else:
        price_rsd = contract_data.price
    price_rsd_in_words = num2words(price_rsd, lang='sr')

    date_context = datetime.strptime(str(contract_data.contract_date), '%Y-%m-%d').strftime('%d.%m.%Y.')

    doc = DocxTemplate(
        current_app.config.get('CONTRACT_TEMPLATE_DIR') + '/' + current_app.config.get('CONTRACT_TEMPLATE'))

    context = {'contract_number': contract_data.contract_number,
               'contract_date': date_context,
               'name': contract_data.name,
               'place': contract_data.place,
               'street': contract_data.street,
               'num': contract_data.num,
               'address': contract_data.address,
               'quadrature': contract_data.quadrature,
               'price_rsd': price_rsd,
               'price_rsd_in_words': price_rsd_in_words,
               }

    doc.render(context)

    file_name = contract_data.address + '-' + str(contract_data.quadrature) + 'kvm'
    doc.save(current_app.config.get('CONTRACT_DIR') +
             '/' + file_name + '.docx')

    message = 'Contract with name ' + file_name + ' created'
    return jsonify({'message': message}), 200
