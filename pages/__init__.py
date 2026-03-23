from flask import Blueprint

pages_bp = Blueprint('pages', __name__, url_prefix='/')

from . import views
