from flask import Blueprint

inscripciones=Blueprint(
    'inscripciones',
    __name__,
    template_folder='templates',
    static_folder='static')
from . import routes
