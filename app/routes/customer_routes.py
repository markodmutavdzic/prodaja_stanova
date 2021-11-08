from flask import Blueprint


cus = Blueprint('apartment', __name__, url_prefix='/customer')


@cus.route('/')
def hello():
    return 'Zdravo, customer', 200