from flask import Blueprint


bp = Blueprint('bp', '__name__')


@bp.route('/123')
def hello():
    return 'Zdravo, zdravo', 200