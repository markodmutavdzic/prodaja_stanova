from datetime import datetime
from functools import wraps

import jwt
from flask import Blueprint, request, current_app, jsonify
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from app.marsh import new_user_schema, edit_user_schema, login_schema
from app.models import db, User

bp = Blueprint('bp', __name__)


@bp.route('/')
def hello():
    return 'Zdravo, zdravo', 200


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid.'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@bp.route('/login', methods=['POST'])
def login():
    auth = login_schema.load(request.get_json())
    user = User.query.filter_by(username=auth['username']).first()
    if not user:
        return jsonify({"message": "User with that username doesn't exist"}), 401
    if check_password_hash(user.password, auth['password']):
        token = jwt.encode(
            {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            current_app.config.get('SECRET_KEY'), algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({"message": "Invalid password"}), 401


@bp.route('/add_new_user', methods=['POST'])
def add_new_user():
    try:
        data = new_user_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    # data = request.get_json()

    user = User.query.filter_by(username=data.get('username')).first()
    if user:
        return jsonify({"message": "User with that username already exists."}), 400

    new_user = User()
    new_user.first_name = data['first_name']
    new_user.last_name = data['last_name']
    new_user.username = data['username']
    new_user.password = generate_password_hash(data['password'], method='sha256')
    new_user.role = data['role']

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "New user created."}), 200


@bp.route('/edit_user', methods=['POST'])
def edit_user():
    data = edit_user_schema.load(request.get_json())

    user = User.query.filter_by(id=data.get('id')).first()
    if not user:
        return jsonify({"message": "User with that id doesnt exists."}), 400

    if data.get('first_name'):
        user.first_name = data['first_name']
    if data.get('last_name'):
        user.last_name = data['last_name']
    if data.get('username'):
        user.username = data['username']
    if data.get('password'):
        user.password = generate_password_hash(data['password'], method='sha256')
    if data.get('role'):
        user.role = data['role']

    db.session.commit()

    return jsonify({"message": "User edited."}), 200


