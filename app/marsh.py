
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
    quadrature = fields.Decimal(required=True)
    floor = fields.Str(required=True, validate=Length(max=50))
    num_rooms = fields.Decimal(required=True)
    orientation = fields.Str(required=True)
    num_terrace = fields.Integer(required=True)
    price = fields.Decimal(required=True)
    status = fields.Str(required=True)
    new_construction = fields.Boolean()
    in_construction = fields.Boolean()
    available_from = fields.Date()


new_apartment_schema = NewApartment()
