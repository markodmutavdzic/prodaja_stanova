
def user_serialize(user_db):
    user = {
        "id": user_db.id,
        "first_name": user_db.first_name,
        "last_name": user_db.last_name,
        "password": "",
        "username": user_db.username,
        "role": user_db.role
    }
    return user


def users_serialize(users):
    result = []
    for user in users:
        user_add = user_serialize(user)
        result.append(user_add)
    return result


def apartment_serialize(apartment_db):
    urls = [image.url for image in apartment_db.images]
    apartment = {
        "id": apartment_db.id,
        "lamella": apartment_db.lamella,
        "address": apartment_db.address,
        "quadrature": apartment_db.quadrature,
        "floor": apartment_db.floor,
        "num_rooms": apartment_db.num_rooms,
        "orientation": apartment_db.orientation,
        "num_terrace": apartment_db.num_terrace,
        "price": apartment_db.price,
        "status": apartment_db.status,
        "new_construction": apartment_db.new_construction,
        "in_construction": apartment_db.in_construction,
        "available_from": str(apartment_db.available_from),
        "images": urls
    }
    return apartment


def apartments_serialize(apartments):
    result = []
    for apartment in apartments:
        apartment_add = apartment_serialize(apartment)
        result.append(apartment_add)
    return result


def customer_serialize(customer_db):
    customer = {
        "id": customer_db.id,
        "legal_entity": customer_db.legal_entity,
        "name": customer_db.name,
        "email": customer_db.email,
        "telephone_number": customer_db.telephone_number,
        "pib_jmbg": customer_db.pib_jmbg,
        "place": customer_db.place,
        "street": customer_db.street,
        "num": customer_db.num,
        "date_of_first_visit": str(customer_db.date_of_first_visit)
    }
    return customer


def customers_serialize(customers):
    result = []
    for customer in customers:
        customer_add = customer_serialize(customer)
        result.append(customer_add)

    return result


def offer_serialize(offer):
    serialized_offer = {
        "id": offer.id,
        "apartment_id": offer.apartment_id,
        "customer_id": offer.customer_id,
        "customer_status": offer.customer_status,
        "customer_price": offer.customer_price,
        "price_approved": offer.price_approved,
        "note": offer.note,
        "currency": offer.currency,
        "payment_method": offer.payment_method,
        "deposit_amount": offer.deposit_amount,
        "contract_deadline": offer.contract_deadline,
        "bank": offer.bank,
        "loan_amount": offer.loan_amount,
        "cash_amount": offer.cash_amount,
        "contract_number": offer.contract_number,
        "contract_date": offer.contract_date
    }

    return serialized_offer


def customer_apartment_serialize(customers_apartments):
    result = []
    for customer, offer in customers_apartments:
        dict_to_append = {}
        cust = customer_serialize(customer)
        off = offer_serialize(offer)
        dict_to_append.update(cust)
        dict_to_append.update(off)
        result.append(dict_to_append)

    return result


def apartment_customer_serialize(apartments_customer):
    result = []
    for apartment, offer in apartments_customer:
        dict_to_append = {}
        apart = apartment_serialize(apartment)
        off = offer_serialize(offer)
        dict_to_append.update(apart)
        dict_to_append.update(off)
        result.append(dict_to_append)

    return result


def price_for_approval_serialize(customers_apartments_price):
    result = []
    for offer in customers_apartments_price:
        dict_to_append = {
            'apartment_customer_id': offer.offer_id,
            'apartment_id': offer.apartment_id,
            'apartment_address': offer.apartment_address,
            'apartment_quadrature': offer.apartment_quadrature,
            'apartment_price': offer.apartment_price,
            'apartment_lowest_price': offer.apartment_lowest_price,
            'apartment_customer_price': offer.apartment_customer_price,
            'price_approved': offer.price_approved,
            'customer_id': offer.customer_id,
            'customer_name': offer.customer_name
        }
        result.append(dict_to_append)

    return result



