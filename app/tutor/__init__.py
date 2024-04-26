from flask import Blueprint

tutor = Blueprint('tutor', __name__, template_folder='../../templates')

from . import views
