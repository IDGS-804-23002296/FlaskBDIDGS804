from . import cursos
from flask import render_template, request, redirect, url_for, flash
import forms
from models import Maestros, db, Curso

@cursos.route("/cursos", methods=['GET', 'POST'])
def index():
    create_form = forms.CursosForm(request.form)
    cursos_list = Curso.query.all()
    return render_template("cursos/listadoCursos.html", form=create_form, cursos=cursos_list)

@cursos.route("/Curso", methods=['GET', 'POST'])
def listadoCursos():
    create_form = forms.CursosForm(request.form)
    
    if request.method == 'POST':
        maestro_seleccionado = create_form.maestro.data
        
        curs = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=maestro_seleccionado.matricula 
        )
        db.session.add(curs)
        db.session.commit()
        return redirect(url_for('cursos.index'))
        
    return render_template("cursos/Curso.html", form=create_form)

@cursos.route("/detallesCursos", methods=['GET', 'POST'])
def detallesCursos():
    id = request.args.get('id')
    curs1 = Curso.query.get_or_404(id)
    
    create_form = forms.CursosForm(request.form)
    create_form.maestro.query_factory = lambda: Maestros.query.all()
    
    if curs1.maestro:
        nombre_maestro = f"{curs1.maestro.nombre} {curs1.maestro.apellidos}"
    else:
        nombre_maestro = "Sin maestro asignado"
        
    return render_template("cursos/detallesCursos.html", 
                           form=create_form, 
                           id=curs1.id,
                           nombre=curs1.nombre, 
                           descripcion=curs1.descripcion, 
                           maestro_nombre=nombre_maestro)

@cursos.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@cursos.route("/modificarCursos", methods=['GET', 'POST'])
def modificarCursos():
    id = request.args.get('id')
    curs = Curso.query.get(id)

    create_form = forms.CursosForm(request.form)
    
    create_form.maestro.query_factory = lambda: Maestros.query.all()
    
    if request.method == 'GET':
        create_form.id.data = curs.id
        create_form.nombre.data = curs.nombre
        create_form.descripcion.data = curs.descripcion
        create_form.maestro.data = curs.maestro 
            
    if create_form.validate_on_submit():
        curs.nombre = create_form.nombre.data
        curs.descripcion = create_form.descripcion.data
        
        if create_form.maestro.data:
            curs.maestro_id = create_form.maestro.data.matricula
            
        db.session.commit()
        return redirect(url_for('cursos.index'))

    return render_template("cursos/modificarCursos.html", form=create_form)

@cursos.route("/eliminarCursos", methods=['GET', 'POST'])
def eliminarCursos():
    id = request.args.get('id')
    curs1 = Curso.query.get(id)

    create_form = forms.CursosForm(request.form)
    
    create_form.maestro.query_factory = lambda: Maestros.query.all()

    if request.method == 'GET':
        create_form.id.data = curs1.id
        create_form.nombre.data = curs1.nombre
        create_form.descripcion.data = curs1.descripcion
        create_form.maestro.data = curs1.maestro
            
    if create_form.validate_on_submit():
        if curs1:
            db.session.delete(curs1)
            db.session.commit()
        return redirect(url_for('cursos.index'))
        
    return render_template("cursos/eliminarCursos.html", form=create_form)