from . import main
import services
from flask import render_template


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html', **services.get_tags())


@main.route('/tag/<int:tag_id>', methods=['GET'])
def tag(tag_id):
    return render_template('tag.html', **services.get_tag_statuses(tag_id))


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
