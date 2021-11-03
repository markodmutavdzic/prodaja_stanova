
from marshmallow import Schema, fields, post_load, validate
from marshmallow.validate import Length, Range


class NewUser(Schema):
    first_name = fields.Str(required=True, validate=Length(max=50))
    last_name = fields.Str(required=True, validate=Length(max=50))
    username = fields.Str(required=True, validate=Length(max=50))
    password = fields.Str(required=True, validate=Length(max=50))
    role = fields.Str(required=True, validate=validate.OneOf(["ADMIN", "PRODAVAC", "FINANSIJE"]))


class EditUser(Schema):
    first_name = fields.Str(validate=Length(max=50))
    last_name = fields.Str(validate=Length(max=50))
    username = fields.Str(validate=Length(max=50))
    password = fields.Str(validate=Length(max=50))
    role = fields.Str(validate=validate.OneOf(["ADMIN", "PRODAVAC", "FINANSIJE"]))


new_user_schema = NewUser()
edit_user_schema = EditUser()

