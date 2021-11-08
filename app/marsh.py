
from marshmallow import Schema, fields, post_load, validate
from marshmallow.validate import Length, Range


class Login(Schema):
    username = fields.Str(required=True, validate=Length(max=50))
    password = fields.Str(required=True, validate=Length(max=50))


login_schema = Login()


class NewUser(Schema):
    first_name = fields.Str(required=True, validate=Length(max=50))
    last_name = fields.Str(required=True, validate=Length(max=50))
    username = fields.Str(required=True, validate=Length(max=50))
    password = fields.Str(required=True, validate=Length(max=50))
    role = fields.Str(required=True, validate=validate.OneOf(["ADMIN", "PRODAVAC", "FINANSIJE"]))


new_user_schema = NewUser()


class EditUser(Schema):
    id = fields.Integer(required=True)
    first_name = fields.Str(validate=Length(max=50))
    last_name = fields.Str(validate=Length(max=50))
    username = fields.Str(validate=Length(max=50))
    password = fields.Str(validate=Length(max=50))
    role = fields.Str(validate=validate.OneOf(["ADMIN", "PRODAVAC", "FINANSIJE"]))


edit_user_schema = EditUser()


class EditCurrentUser(Schema):
    first_name = fields.Str(validate=Length(max=50))
    last_name = fields.Str(validate=Length(max=50))
    username = fields.Str(validate=Length(max=50))
    password = fields.Str(validate=Length(max=50))


edit_current_user_schema = EditCurrentUser()


class NewApartment(Schema):
    lamella = fields.Str(validate=Length(max=50))
    address = fields.Str(required=True, validate=Length(max=100))
    quadrature = fields.Decimal(required=True)
    floor = fields.Integer(required=True)
    num_rooms = fields.Decimal(required=True)
    orientation = fields.Str(required=True, validate=validate.OneOf(["ISTOK", "ZAPAD", "SEVER", "JUG"]))
    num_terrace = fields.Integer(required=True)
    price = fields.Decimal(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["SLOBODAN", "REZERVISAN", "PRODAT"]))
    new_construction = fields.Boolean()
    in_construction = fields.Boolean()
    available_from = fields.Date()


new_apartment_schema = NewApartment()


class EditApartment(Schema):
    id = fields.Integer(required=True)
    lamella = fields.Str(validate=Length(max=50))
    address = fields.Str(validate=Length(max=100))
    quadrature = fields.Decimal()
    floor = fields.Integer()
    num_rooms = fields.Decimal()
    orientation = fields.Str(validate=validate.OneOf(["ISTOK", "ZAPAD", "SEVER", "JUG"]))
    num_terrace = fields.Integer()
    price = fields.Decimal()
    status = fields.Str(validate=validate.OneOf(["SLOBODAN", "REZERVISAN", "PRODAT"]))
    new_construction = fields.Boolean()
    in_construction = fields.Boolean()
    available_from = fields.Date()


edit_apartment_schema = EditApartment()


class FilterApartment(Schema):
    lamella = fields.Str(validate=Length(max=50))
    address = fields.Str(validate=Length(max=100))
    quadrature_from = fields.Decimal()
    quadrature_to = fields.Decimal()
    floor_from = fields.Integer()
    floor_to = fields.Integer()
    num_rooms_from = fields.Decimal()
    num_rooms_to = fields.Decimal()
    orientation = fields.Str(validate=validate.OneOf(["ISTOK", "ZAPAD", "SEVER", "JUG"]))
    num_terrace_from = fields.Integer()
    num_terrace_to = fields.Integer()
    price_from = fields.Decimal()
    price_to = fields.Decimal()
    status = fields.Str(validate=validate.OneOf(["SLOBODAN", "REZERVISAN", "PRODAT"]))
    new_construction = fields.Boolean()
    in_construction = fields.Boolean()
    available_from_from = fields.Date()
    available_from_to = fields.Date()
    order_id = fields.Str(validate=validate.OneOf(["ASC", "DESC"]))
    order_price = fields.Str(validate=validate.OneOf(["ASC", "DESC"]))


filter_apartment_schema = FilterApartment()