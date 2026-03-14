from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
import forms
from models import db, Alumno
from maestros.routes import maestros
from cursos.routes import cursos
from inscripciones.routes import inscripciones
from alumnos.routes import alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(maestros)
app.register_blueprint(cursos)
app.register_blueprint(inscripciones)
app.register_blueprint(alumnos)

db.init_app(app)
migrate = Migrate(app, db)
app.secret_key = 'clave_secreta'
csrf = CSRFProtect(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/", methods=['GET'])
@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)