from flask import Blueprint

apa = Blueprint('apartment', __name__, url_prefix='/apartment')


@apa.route('/')
def hello():
    return 'Zdravo, apartment', 200



