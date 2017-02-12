# app/admin/__init__.py

from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import department_view
from . import role_view
from . import employee_view