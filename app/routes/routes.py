from datetime import date

from flask import Blueprint

from app import enums
from app.models import Kupac, db, Stan

bp = Blueprint('bp', '__name__')



@bp.route('/123')
def hello():




    return 'Zdravo, zdravo', 200