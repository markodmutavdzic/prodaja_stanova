from datetime import date

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import func

from app import enums
from app.marsh import report_schema, customer_report_schema
from app.models import Apartment, ApartmentCustomer, db, Customer
from app.serialize import apartment_customer_serialize, customer_serialize

rep = Blueprint('report', __name__, url_prefix='/report')


@rep.route('/')
def hello():
    return 'Zdravo, report', 200


@rep.route('/apartment_status', methods=['POST'])
def apartment_status_report():
    try:
        data = report_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    date_from = data.get('date_from')
    date_to = data.get('date_to')

    if date_from and not date_to:
        date_to = date.today()
    if date_to and not date_from:
        return {'message': 'Date from required'}, 400

    if not date_from and not date_to:
        available = Apartment.query.filter(Apartment.status == enums.Status.SLOBODAN)
        reserved = Apartment.query.filter(Apartment.status == enums.Status.REZERVISAN)
        sold = Apartment.query.filter(Apartment.status == enums.Status.PRODAT)

    if date_from and date_to:
        available = Apartment.query.filter(Apartment.date_created >= date_from,
                                           Apartment.date_created <= date_to,
                                           (db.or_(Apartment.date_reserved.is_(None), Apartment.date_reserved > date_to)),
                                           (db.or_(Apartment.date_sold.is_(None), Apartment.date_sold > date_to)))
        reserved = Apartment.query.filter(Apartment.date_reserved >= date_from,
                                          Apartment.date_reserved <= date_to,
                                          (db.or_(Apartment.date_sold.is_(None), Apartment.date_sold > date_to)))
        sold = Apartment.query.filter(Apartment.date_sold >= date_from,
                                      Apartment.date_sold <= date_to)

    available = available.count()
    reserved = reserved.count()
    sold = sold.count()

    return jsonify({'slobodni': available, 'rezervisani': reserved, 'prodati': sold}), 200


@rep.route('/apartments_sold', methods=['POST'])
def apartments_sold():
    try:
        data = report_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    date_from = data.get('date_from')
    date_to = data.get('date_to')

    if date_from and not date_to:
        date_to = date.today()
    if date_to and not date_from:
        return {'message': 'Date from required'}, 400

    apartments_sold_price = db.session.query(func.count(Apartment.id).label('num_of_apartment'),
                                             func.sum(Apartment.price).label('apartment_price'),
                                             func.sum(ApartmentCustomer.customer_price).label('customer_price')) \
        .join(Apartment, Apartment.id == ApartmentCustomer.apartment_id) \
        .filter(ApartmentCustomer.customer_status == enums.CostumerStatus.KUPIO) \
        .filter(Apartment.status == enums.Status.PRODAT)

    if date_from and date_to:
        apartments_sold_price = apartments_sold_price.filter(Apartment.date_sold >= date_from,
                                                             Apartment.date_sold <= date_to)

    apartments_sold_price = apartments_sold_price.all()
    if apartments_sold_price[0]['apartment_price'] and apartments_sold_price[0]['customer_price']:
        price_difference = apartments_sold_price[0]['apartment_price'] - apartments_sold_price[0]['customer_price']

        return jsonify({'aprtments_sold': apartments_sold_price[0]['num_of_apartment'],
                        'price_difference': price_difference}), 200
    return jsonify({'aprtments_sold': 'No apartments sold for that period'}), 200


@rep.route('/apartment_for_customer', methods=['POST'])
def apartment_for_customer():
    try:
        data = customer_report_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    customer_db = Customer.query.filter(Customer.id == data.get('id')).first()
    if not customer_db:
        return jsonify({'message': 'Customer with that id doesnt exists.'}), 400

    apartments_customer = db.session.query(Apartment, ApartmentCustomer) \
        .join(ApartmentCustomer, ApartmentCustomer.apartment_id == Apartment.id). \
        filter(ApartmentCustomer.customer_id == data.get('id'),
               ApartmentCustomer.customer_status == enums.CostumerStatus.POTENCIJALNI) \
        .paginate(per_page=2, page=data.get('page_num'), error_out=True)

    customer = customer_serialize(customer_db)

    result = apartment_customer_serialize(apartments_customer.items)

    return jsonify({"current page": apartments_customer.page,
                    "next_page": apartments_customer.next_num,
                    "perv_page": apartments_customer.prev_num},
                   {'customer': customer},
                   {'apartments_for_customer': result}), 200


@rep.route('/apartments_customer_bought', methods=['POST'])
def apartments_customer_bought():
    try:
        data = customer_report_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    date_from = data.get('date_from')
    date_to = data.get('date_to')

    if date_from and not date_to:
        date_to = date.today()
    if date_to and not date_from:
        return {'message': 'Date from required'}, 400

    customer_db = Customer.query.filter(Customer.id == data.get('id')).first()
    if not customer_db:
        return jsonify({'message': 'Customer with that id doesnt exists.'}), 400

    apartments_customer = db.session.query(Apartment, ApartmentCustomer) \
        .join(ApartmentCustomer, ApartmentCustomer.apartment_id == Apartment.id). \
        filter(ApartmentCustomer.customer_id == data.get('id'),
               ApartmentCustomer.customer_status == enums.CostumerStatus.KUPIO)

    if date_from and date_to:
        apartments_customer = apartments_customer.filter(Apartment.date_sold > date_from,
                                                         Apartment.date_sold <= date_to)

    apartments_customer = apartments_customer.paginate(per_page=2, page=data.get('page_num'), error_out=True)

    result = apartment_customer_serialize(apartments_customer.items)
    customer = customer_serialize(customer_db)
    return jsonify({"current page": apartments_customer.page,
                    "next_page": apartments_customer.next_num,
                    "perv_page": apartments_customer.prev_num},
                   {'customer': customer},
                   {'apartments_customer_bought': result}), 200
