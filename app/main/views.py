from . import main
import services
from flask import render_template


@main.route('/')
def index():
    return render_template('index.html', **services.get_tags())
