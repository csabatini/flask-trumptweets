from flask import Flask
from flask_moment import Moment

moment = Moment()


def create_app():
    app = Flask(__name__)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    moment.init_app(app)

    return app
