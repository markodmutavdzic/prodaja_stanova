

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
        "available_from": str(apartment_db.available_from)
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
