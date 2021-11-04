

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
        user_add = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": "",
            "username": user.username,
            "role": user.role
                }
        result.append(user_add)

    return result
