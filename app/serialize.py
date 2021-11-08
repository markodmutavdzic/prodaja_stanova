

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
