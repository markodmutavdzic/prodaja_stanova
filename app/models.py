from flask_sqlalchemy import SQLAlchemy

from app.enums import UserRole, Orientation, Status, LegalEntity,\
    CostumerStatus, Currency, PaymentMethod

db = SQLAlchemy()


class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)


class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lamella = db.Column(db.String(50))
    quadrature = db.Column(db.DECIMAL, nullable=False)
    floor = db.Column(db.String(50), nullable=False)
    num_rooms = db.Column(db.DECIMAL, nullable=False)
    orientation = db.Column(db.Enum(Orientation))
    num_terrace = db.Column(db.Integer, nullable=False)
    price = db.Column(db.DECIMAL, nullable=False)
    status = db.Column(db.Enum(Status), default=Status.SLOBODAN)
    new_construction = db.Column(db.Boolean)
    in_construction = db.Column(db.Boolean)
    available_from = db.Column(db.Date)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    legal_entity = db.Column(db.Enum(LegalEntity), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telephone_number = db.Column(db.String(100), nullable=False)
    pib_jmbg = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    num = db.Column(db.String(100), nullable=False)
    date_of_first_visit = db.Column(db.Date)


class ApartmentCustomer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'))
    customer_status = db.Column(db.Enum(CostumerStatus))
    customer_price = db.Column(db.DECIMAL)
    price_approved = db.Column(db.Boolean)
    note = db.Column(db.Text())
    currency = db.Column(db.Enum(Currency))
    payment_method = db.Column(db.Enum(PaymentMethod))
    deposit_amount = db.Column(db.DECIMAL)
    contract_deadline = db.Column(db.Date)
    bank = db.Column(db.String(50))
    loan_amount = db.Column(db.DECIMAL)
    cash_aount = db.Column(db.DECIMAL)
    contract_number = db.Column(db.String(100))
    contract_date = db.Column(db.Date)











