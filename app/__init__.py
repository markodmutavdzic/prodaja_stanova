from flask_migrate import Migrate
from app.models import db
from app.routes.apartment_customer_routes import apc
from app.routes.apartment_routes import apa
from app.routes.customer_routes import cus
from app.routes.report_routes import rep
from app.routes.user_routes import usr
from flask import Flask
from swagger.swagger_config import SWAGGERUI_BLUEPRINT, SWAGGER_URL

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.register_blueprint(usr)
    app.register_blueprint(apa)
    app.register_blueprint(cus)
    app.register_blueprint(apc)
    app.register_blueprint(rep)
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    app.config.from_json('../config.json')

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def hello():
        return 'Zdravo, zdravo', 200

    return app
