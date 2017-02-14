from flask import Blueprint

teaching_fellow = Blueprint('teaching_fellow', __name__)

from . import views