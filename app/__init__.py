from flask import Flask
from flask_moment import Moment
from main import main as main_blueprint

moment = Moment()


def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_blueprint)

    moment.init_app(app)

    return app
