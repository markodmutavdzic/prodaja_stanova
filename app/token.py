from functools import wraps

import jwt
from flask import request, jsonify, current_app

from app.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers.get('access-token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            current_user = User.query.filter_by(id=data.get('id')).first()
        except:
            return jsonify({'message': 'Token is invalid.'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
