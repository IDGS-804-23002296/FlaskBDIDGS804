from flask import Blueprint

alumnos=Blueprint(
    'alumnos',
    __name__,
    template_folder='templates',
    static_folder='static')
from . import routes
