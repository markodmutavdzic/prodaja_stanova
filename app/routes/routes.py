from flask import Blueprint

bp = Blueprint('bp', '__name__')


@bp.route('/')
def hello():
    return 'Zdravo, zdravo', 200