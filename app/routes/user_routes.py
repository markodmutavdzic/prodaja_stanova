import datetime
import jwt
from flask import Blueprint, request, current_app, jsonify
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from app import enums
from app.marsh import new_user_schema, edit_user_schema, login_schema, edit_current_user_schema, search_user_schema, \
    id_schema

from app.models import db, User
from app.token import token_required
from app.serialize import users_serialize, user_serialize

usr = Blueprint('user', __name__, url_prefix='/user')


@usr.route('/')
def hello():
    return 'Zdravo, user', 200


@usr.route('/login', methods=['POST'])
def login():
    auth = login_schema.load(request.get_json())
    user = User.query.filter(User.username == auth.get('username')).first()
    if not user:
        return jsonify({'message': 'User with that username doesnt exist'}), 401
    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode(
            {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)},
            current_app.config.get('SECRET_KEY'), algorithm='HS256')
        user_f = user_serialize(user)
        return jsonify({'token': token}, {'user': user_f}), 200
    return jsonify({'message': 'Invalid password'}), 401


@usr.route('/add', methods=['POST'])
@token_required
def add_new_user(current_user):
# def add_new_user():
    if current_user.role is not enums.UserRole.ADMIN:
        return jsonify({'message': 'User must be ADMIN'}), 400

    try:
        data = new_user_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    user = User.query.filter(User.username == data.get('username')).first()
    if user:
        return jsonify({'message': 'User with that username already exists.'}), 400

    new_user = User()
    new_user.first_name = data.get('first_name')
    new_user.last_name = data.get('last_name')
    new_user.username = data.get('username')
    new_user.password = generate_password_hash(data.get('password'), method='sha256')
    new_user.role = data.get('role')

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created.'}), 200


@usr.route('/edit', methods=['POST'])
@token_required
def edit_user(current_user):
# def edit_user():
    if current_user.role is not enums.UserRole.ADMIN:
        return jsonify({'message': 'User must be ADMIN'}), 400

    try:
        data = edit_user_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    user = User.query.filter(User.id == data.get('id')).first()
    if not user:
        return jsonify({'message': 'User with that id doesnt exists.'}), 400

    if data.get('username'):
        check_user = User.query.filter(User.username == data.get('username')).first()
        if check_user and (check_user.id != user.id):
            return jsonify({'message': 'User with that username already exists.'}), 400
        user.username = data.get('username')
    if data.get('first_name'):
        user.first_name = data.get('first_name')
    if data.get('last_name'):
        user.last_name = data.get('last_name')
    if data.get('password'):
        user.password = generate_password_hash(data.get('password'), method='sha256')
    if data.get('role'):
        user.role = data.get('role')

    db.session.commit()

    return jsonify({'message': 'User edited.'}), 200


@usr.route('/edit_current', methods=['POST'])
@token_required
def edit_current_user(current_user):

    try:
        data = edit_current_user_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    user = current_user

    if data.get('username'):
        check_user = User.query.filter(User.username == data.get('username')).first()
        if check_user and (check_user.id != user.id):
            return jsonify({'message': 'User with that username already exists.'}), 400
        user.username = data.get('username')
    if data.get('first_name'):
        user.first_name = data.get('first_name')
    if data.get('last_name'):
        user.last_name = data.get('last_name')
    if data.get('password'):
        user.password = generate_password_hash(data.get('password'), method='sha256')
    if data.get('role'):
        user.role = data.get('role')

    db.session.commit()

    return jsonify({'message': 'Current user edited.'}), 200


@usr.route('/all', methods=['POST'])
@token_required
def all_users(current_user):
    if current_user.role is not enums.UserRole.ADMIN:
        return jsonify({'message': 'User must be ADMIN'}), 400
# def all_users():
    try:
        data = search_user_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400
    users = User.query

    if data.get('username'):
        users = users.filter(User.username.ilike('%' + data.get('username') + '%'))
    if data.get('first_name'):
        users = users.filter(User.first_name.ilike('%' + data.get('first_name') + '%'))
    if data.get('last_name'):
        users = users.filter(User.last_name.ilike('%' + data.get('last_name') + '%'))
    if data.get('role'):
        users = users.filter(User.role == (data.get('role')))

    users = users.paginate(per_page=2, page=data.get('page_num'), error_out=True)

    result = users_serialize(users.items)
    return jsonify({"current page": users.page,
                    "next_page": users.next_num,
                    "perv_page": users.prev_num},
                   {'users': result}), 200


@usr.route('/delete', methods=['POST'])
@token_required
# def delete_user():
def delete_user(current_user):
    if current_user.role is not enums.UserRole.ADMIN:
        return jsonify({'message': 'User must be ADMIN'}), 400

    try:
        data = id_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    user_for_delete = User.query.filter(User.id == data.get('id')).first()
    if not user_for_delete:
        return jsonify({'message': 'User with that id doesnt exists.'}), 400

    db.session.delete(user_for_delete)
    db.session.commit()

    return jsonify({'message': 'User deleted'}), 200



