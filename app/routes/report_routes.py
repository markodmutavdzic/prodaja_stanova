from flask import Blueprint

rep = Blueprint('report', __name__, url_prefix='/report')

@rep.route("/")
def hello():
    return 'Zdravo, report', 200



@rep.route("/apartment_status")
def apartment_status_report():
    return "123"