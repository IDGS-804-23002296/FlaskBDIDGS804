from . import alumnos
from flask import render_template, request, redirect, url_for, flash
import forms
from models import db, Alumno, Curso

@alumnos.route("/alumnos", methods=['GET', 'POST'])
def index():
    create_form = forms.UserForm(request.form)
    alumnos_list = Alumno.query.all()
    return render_template("alumnos/listadoAlum.html", form=create_form, alumnos=alumnos_list)

@alumnos.route("/Alumnos", methods=['GET', 'POST'])
def listadoAlumno():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'POST':
        alum = Alumno(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.email.data,
            telefono=create_form.telefono.data
        )
        try:
            db.session.add(alum)
            db.session.commit()
            return redirect(url_for('alumnos.index'))
        except Exception as e:
            db.session.rollback()
            flash("Error al guardar en la base de datos")
            
    return render_template("alumnos/Alumnos.html", form=create_form)

@alumnos.route("/detallesAlumno", methods=['GET', 'POST'])
def detallesAlumno():
    create_form = forms.UserForm(request.form)
    id = request.args.get('id')
    alum1 = db.session.query(Alumno).filter(Alumno.id == id).first()
    
    if not alum1:
        return "Alumno no encontrado", 404
        
    return render_template("alumnos/detalles.html", 
                           form=create_form, 
                           id=id, 
                           nombre=alum1.nombre, 
                           apellidos=alum1.apellidos, 
                           email=alum1.email, 
                           telefono=alum1.telefono)

@alumnos.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id') 
        alum1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        
        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apellidos.data = alum1.apellidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono
        else:
            return "Alumno no encontrado", 404
            
    if create_form.validate_on_submit():
        id = create_form.id.data
        alum1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        
        if alum1:
            alum1.nombre = create_form.nombre.data
            alum1.apellidos = create_form.apellidos.data
            alum1.email = create_form.email.data
            alum1.telefono = create_form.telefono.data
            
            db.session.add(alum1)
            db.session.commit()
            return redirect(url_for('alumnos.index'))
        else:
            return "Error al intentar actualizar: Alumno no existe", 404

    return render_template("alumnos/modificar.html", form=create_form)

@alumnos.route("/eliminar", methods=['GET', 'POST'])
def eliminarAlumno():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apellidos.data = alum1.apellidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono
        else:
            return "Alumno no encontrado", 404
            
    if create_form.validate_on_submit():
        id = create_form.id.data
        alum1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        if alum1:
            db.session.delete(alum1)
            db.session.commit()
        return redirect(url_for('alumnos.index'))
        
    return render_template("alumnos/eliminar.html", form=create_form)

@alumnos.route("/listaAlumnos")
def listaAlumnos():
    id_alumno = request.args.get('id')
    todos = Alumno.query.all() # Necesario para llenar el select
    
    alumno = None
    cursos_del_alumno = []
    
    if id_alumno:
        alumno = Alumno.query.get(id_alumno)
        if alumno:
            cursos_del_alumno = alumno.cursos
            
    return render_template("alumnos/listaAlumnos.html", 
                           todos_los_alumnos=todos,
                           alumno=alumno, 
                           cursos=cursos_del_alumno)

@alumnos.route("/listaCursos")
def listaCursos():
    id_curso = request.args.get('id')
    todos = Curso.query.all() 
    
    curso = None
    alumnos_inscritos = []
    
    if id_curso:
        curso = Curso.query.get(id_curso)
        if curso:
            alumnos_inscritos = curso.alumnos
            
    return render_template("alumnos/listaCursos.html", 
                           todos_los_cursos=todos,
                           curso=curso, 
                           alumnos=alumnos_inscritos)