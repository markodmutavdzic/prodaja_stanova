from flask_sqlalchemy import SQLAlchemy

from app.enums import UserRole, Orientation, Status, LegalEntity,\
    CostumerStatus, Currency, PaymentMethod

db = SQLAlchemy()


class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)


class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lamella = db.Column(db.String(50))
    address = db.Column(db.String(100), nullable=False)
    quadrature = db.Column(db.DECIMAL, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    num_rooms = db.Column(db.DECIMAL, nullable=False)
    orientation = db.Column(db.Enum(Orientation))
    num_terrace = db.Column(db.Integer, nullable=False)
    price = db.Column(db.DECIMAL, nullable=False)
    lowest_price = db.Column(db.DECIMAL, nullable=False)
    status = db.Column(db.Enum(Status), default=Status.SLOBODAN)
    new_construction = db.Column(db.Boolean, default=False)
    in_construction = db.Column(db.Boolean)
    available_from = db.Column(db.Date)
    images = db.relationship("Image", back_populates='apartment', cascade="all, delete-orphan")


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    legal_entity = db.Column(db.Enum(LegalEntity), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telephone_number = db.Column(db.String(100), nullable=False)
    pib_jmbg = db.Column(db.String(50), nullable=False, unique=True)
    place = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    num = db.Column(db.String(100), nullable=False)
    date_of_first_visit = db.Column(db.Date)


class ApartmentCustomer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id', ondelete='CASCADE'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'))
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
    cash_amount = db.Column(db.DECIMAL)
    contract_number = db.Column(db.String(100))
    contract_date = db.Column(db.Date)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, default=None)
    location = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id', ondelete='CASCADE'))
    apartment = db.relationship("Apartment", back_populates='images')








