from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routes.apartment_routes import apa
from app.routes.user_routes import usr

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.register_blueprint(usr)
    app.register_blueprint(apa)
    app.config.from_json('../config.json')

    db.init_app(app)
    migrate.init_app(app, db)

    return app
