from datetime import date

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app import enums
from app.marsh import report_schema
from app.models import Apartment

rep = Blueprint('report', __name__, url_prefix='/report')

@rep.route("/")
def hello():
    return 'Zdravo, report', 200



@rep.route("/apartment_status", methods=['POST'])
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
        return {'message': "Date from required"}, 400

    if not date_from and not date_to:
        available = Apartment.query.filter(Apartment.status == enums.Status.SLOBODAN).count()
        reserved = Apartment.query.filter(Apartment.status == enums.Status.REZERVISAN).count()
        sold = Apartment.query.filter(Apartment.status == enums.Status.PRODAT).count()

    elif date_from and date_to:
        available = Apartment.query.filter(Apartment.date_created > date_from, Apartment.date_created <= date_to,
                                           Apartment.date_reserved.is_(None), Apartment.date_sold.is_(None)).count()
        reserved = Apartment.query.filter(Apartment.date_reserved > date_from, Apartment.date_reserved <= date_to,
                                          Apartment.date_sold.is_(None)).count()
        sold = Apartment.query.filter(Apartment.date_sold > date_from, Apartment.date_sold <= date_to).count()

    return jsonify({'slobodni': available, 'rezervisani': reserved, 'prodati': sold}), 200