
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
    role = fields.Str(required=True, validate=validate.OneOf(['ADMIN', 'PRODAVAC', 'FINANSIJE']))


new_user_schema = NewUser()


class EditUser(Schema):
    id = fields.Integer(required=True)
    first_name = fields.Str(validate=Length(max=50))
    last_name = fields.Str(validate=Length(max=50))
    username = fields.Str(validate=Length(max=50))
    password = fields.Str(validate=Length(max=50))
    role = fields.Str(validate=validate.OneOf(['ADMIN', 'PRODAVAC', 'FINANSIJE']))


edit_user_schema = EditUser()


class SearchUser(Schema):
    first_name = fields.Str(validate=Length(max=50))
    last_name = fields.Str(validate=Length(max=50))
    username = fields.Str(validate=Length(max=50))
    role = fields.Str(validate=validate.OneOf(['ADMIN', 'PRODAVAC', 'FINANSIJE']))
    page_num = fields.Integer()

search_user_schema = SearchUser()


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
    orientation = fields.Str(required=True, validate=validate.OneOf(['ISTOK', 'ZAPAD', 'SEVER', 'JUG']))
    num_terrace = fields.Integer(required=True)
    price = fields.Decimal(required=True)
    lowest_price = fields.Decimal(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['SLOBODAN', 'REZERVISAN', 'PRODAT']))
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
    orientation = fields.Str(validate=validate.OneOf(['ISTOK', 'ZAPAD', 'SEVER', 'JUG']))
    num_terrace = fields.Integer()
    price = fields.Decimal()
    lowest_price = fields.Decimal()
    status = fields.Str(validate=validate.OneOf(['SLOBODAN', 'REZERVISAN', 'PRODAT']))
    new_construction = fields.Boolean()
    in_construction = fields.Boolean()
    available_from = fields.Date()
    lowest_price = fields.Decimal()


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
    orientation = fields.Str(validate=validate.OneOf(['ISTOK', 'ZAPAD', 'SEVER', 'JUG']))
    num_terrace_from = fields.Integer()
    num_terrace_to = fields.Integer()
    price_from = fields.Decimal()
    price_to = fields.Decimal()
    status = fields.Str(validate=validate.OneOf(['SLOBODAN', 'REZERVISAN', 'PRODAT']))
    new_construction = fields.Boolean()
    in_construction = fields.Boolean()
    available_from_from = fields.Date()
    available_from_to = fields.Date()
    order_id = fields.Str(validate=validate.OneOf(['ASC', 'DESC']))
    order_price = fields.Str(validate=validate.OneOf(['ASC', 'DESC']))
    page_num = fields.Integer()

filter_apartment_schema = FilterApartment()


class NewCustomer(Schema):
    legal_entity = fields.Str(validate=validate.OneOf(['FIZICKO', 'PRAVNO']), required=True)
    name = fields.Str(required=True, validate=Length(max=50))
    email = fields.Email()
    telephone_number = fields.Str(required=True, validate=Length(max=100))
    pib_jmbg = fields.Str(required=True, validate=Length(max=50))
    place = fields.Str(required=True, validate=Length(max=100))
    street = fields.Str(required=True, validate=Length(max=100))
    num = fields.Str(required=True, validate=Length(max=100))


new_customer_schema = NewCustomer()


class EditCustomer(Schema):
    id = fields.Integer(required=True)
    legal_entity = fields.Str(validate=validate.OneOf(['FIZICKO', 'PRAVNO']))
    name = fields.Str(validate=Length(max=50))
    email = fields.Email()
    telephone_number = fields.Str(validate=Length(max=100))
    pib_jmbg = fields.Str(validate=Length(max=50))
    place = fields.Str(validate=Length(max=100))
    street = fields.Str(validate=Length(max=100))
    num = fields.Str(validate=Length(max=100))


edit_customer_schema = EditCustomer()


class SearchCustomer(Schema):
    legal_entity = fields.Str(validate=validate.OneOf(['FIZICKO', 'PRAVNO']))
    name = fields.Str(validate=Length(max=50))
    email = fields.Email()
    telephone_number = fields.Str(validate=Length(max=100))
    pib_jmbg = fields.Str(validate=Length(max=50))
    place = fields.Str(validate=Length(max=100))
    street = fields.Str(validate=Length(max=100))
    num = fields.Str(validate=Length(max=100))
    date_of_first_visit_from = fields.Date()
    date_of_first_visit_to = fields.Date()
    page_num = fields.Integer()

search_customer_schema = SearchCustomer()


class NewApartmentCustomer(Schema):
    apartment_id = fields.Integer(required=True)
    customer_id = fields.Integer(required=True)
    customer_status = fields.Str(required=True, validate=validate.OneOf(['POTECNCIJALNI', 'REZERVISAO', 'KUPIO']))
    customer_price = fields.Decimal(required=True)
    note = fields.Str()
    payment_method = fields.Str(validate=validate.OneOf(['KES', 'KREDIT', 'MESOVITO']))
    deposit_amount = fields.Decimal()
    contract_deadline = fields.Date()
    bank = fields.Str()
    loan_amount = fields.Decimal()
    cash_amount = fields.Decimal()
    contract_number = fields.Str()
    contract_date = fields.Date()


new_apartment_customer_schema = NewApartmentCustomer()


class EditApartmentCustomer(Schema):
    id = fields.Integer(required=True)
    apartment_id = fields.Integer()
    customer_id = fields.Integer()
    customer_status = fields.Str(validate=validate.OneOf(['POTECNCIJALNI', 'REZERVISAO', 'KUPIO']))
    customer_price = fields.Decimal()
    note = fields.Str()
    payment_method = fields.Str(validate=validate.OneOf(['KES', 'KREDIT', 'MESOVITO']))
    deposit_amount = fields.Decimal()
    contract_deadline = fields.Date()
    bank = fields.Str()
    loan_amount = fields.Decimal()
    cash_amount = fields.Decimal()
    contract_number = fields.Str()
    contract_date = fields.Date()


edit_apartment_customer_schema = EditApartmentCustomer()


class EditApartmentCustomerForSale(Schema):
    id = fields.Integer(required=True)
    customer_status = fields.Str(validate=validate.OneOf(['POTECNCIJALNI', 'REZERVISAO', 'KUPIO']))
    customer_price = fields.Decimal()
    note = fields.Str()


edit_apartment_customer_for_sale_schema = EditApartmentCustomerForSale()


class EditApartmentCustomerForContract(Schema):
    id = fields.Integer(required=True)
    payment_method = fields.Str(validate=validate.OneOf(['KES', 'KREDIT', 'MESOVITO']))
    deposit_amount = fields.Decimal()
    contract_deadline = fields.Date()
    bank = fields.Str()
    loan_amount = fields.Decimal()
    cash_amount = fields.Decimal()
    contract_number = fields.Str()
    contract_date = fields.Date()


edit_apartment_customer_for_contract_schema = EditApartmentCustomerForContract()


class Id(Schema):

    id = fields.Integer(required=True)
    page_num = fields.Integer()


id_schema = Id()


class PriceApproved(Schema):
    id = fields.Integer(required=True)
    price_approved = fields.Boolean(required=True)


price_approved_schema = PriceApproved()


class ImagesDelete(Schema):
    apartment_id = fields.Integer(required=True)
    urls = fields.List(cls_or_instance=fields.Str())


images_delete_schema = ImagesDelete()


class Report(Schema):

    date_from = fields.Date()
    date_to = fields.Date()


report_schema = Report()


class CustomerReport(Schema):

    date_from = fields.Date()
    date_to = fields.Date()
    id = fields.Integer(required=True)
    page_num = fields.Integer()


customer_report_schema = CustomerReport()


class PriceApproval(Schema):

    page_num = fields.Integer()


price_approval_schema = PriceApproval()