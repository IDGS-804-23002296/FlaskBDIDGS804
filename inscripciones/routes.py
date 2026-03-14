from . import inscripciones
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
import forms
from models import Alumno, Maestros, db, Curso, Inscripcion

@inscripciones.route("/inscripciones", methods=['GET', 'POST'])
def index():
    create_form = forms.InscripcionForm(request.form)
    inscripciones_list = Inscripcion.query.all()
    return render_template("inscripciones/listadoInscripciones.html", form=create_form, inscripciones=inscripciones_list)

@inscripciones.route("/Inscripcion", methods=['GET', 'POST'])
def inscribir_alumno():
    form = forms.InscripcionForm(request.form)
    
    form.alumno.query_factory = lambda: Alumno.query.all()
    form.curso.query_factory = lambda: Curso.query.all()
    
    if request.method == 'GET':
        form.fecha_inscripcion.data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if form.validate_on_submit():
        alumno_obj = form.alumno.data
        curso_obj = form.curso.data
        
        if alumno_obj and curso_obj:
            nueva_inscripcion = Inscripcion(
                alumno_id=alumno_obj.id,
                curso_id=curso_obj.id,
                fecha_inscripcion=form.fecha_inscripcion.data
            )
            
            try:
                db.session.add(nueva_inscripcion)            
                db.session.commit()
                return redirect(url_for('inscripciones.index'))
            except Exception as e:
                db.session.rollback()
        
    return render_template("inscripciones/Inscripcion.html", form=form)

@inscripciones.route("/detallesInscripciones", methods=['GET', 'POST'])
def detallesInscripciones():
    id = request.args.get('id')
    insc = Inscripcion.query.get_or_404(id)
    
    create_form = forms.InscripcionForm()
    create_form.alumno.query_factory = lambda: Alumno.query.all()
    create_form.curso.query_factory = lambda: Curso.query.all()
    
    maestro = insc.curso.maestro if insc.curso and insc.curso.maestro else None
    nombre_maestro = f"{maestro.nombre} {maestro.apellidos}" if maestro else "Sin maestro asignado"
        
    return render_template("inscripciones/detallesInscripciones.html", 
                           form=create_form, 
                           id=insc.id,
                           Alumno=insc.alumno, 
                           Curso=insc.curso, 
                           maestro_nombre=nombre_maestro,
                           fecha_inscripcion=insc.fecha_inscripcion)

@inscripciones.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@inscripciones.route("/modificarInscripciones", methods=['GET', 'POST'])
def modificarInscripciones():
    id = request.args.get('id')
    inscripcion = Inscripcion.query.get_or_404(id)

    form = forms.InscripcionForm(request.form, obj=inscripcion)
    
    form.alumno.query_factory = lambda: Alumno.query.all()
    form.curso.query_factory = lambda: Curso.query.all()
    
    if request.method == 'GET':
        form.id.data = inscripcion.id
        form.alumno.data = inscripcion.alumno
        form.curso.data = inscripcion.curso
        if inscripcion.fecha_inscripcion:
            form.fecha_inscripcion.data = inscripcion.fecha_inscripcion.strftime('%Y-%m-%dT%H:%M')

    if form.validate_on_submit():
        inscripcion.alumno = form.alumno.data
        inscripcion.curso = form.curso.data
        
        try:
            db.session.commit()
            return redirect(url_for('inscripciones.index'))
        except Exception as e:
            db.session.rollback()
            flash("Error: Es posible que el alumno ya esté inscrito en ese curso.")
            print(f"Error: {e}")

    return render_template("inscripciones/modificarInscripciones.html", form=form)

@inscripciones.route("/eliminarInscripciones", methods=['GET', 'POST'])
def eliminarInscripciones():
    id = request.args.get('id')
    ins = Inscripcion.query.get_or_404(id)
    form = forms.InscripcionForm(request.form)

    form.alumno.query_factory = lambda: Alumno.query.all()
    form.curso.query_factory = lambda: Curso.query.all()

    if request.method == 'GET':
        form.id.data = ins.id
        form.alumno.data = ins.alumno
        form.curso.data = ins.curso
        if ins.fecha_inscripcion:
            form.fecha_inscripcion.data = ins.fecha_inscripcion.strftime('%Y-%m-%d %H:%M:%S')
            
    if form.validate_on_submit():
        try:
            db.session.delete(ins)
            db.session.commit()
            return redirect(url_for('inscripciones.index'))
        except Exception as e:
            db.session.rollback()
        
    return render_template("inscripciones/eliminarInscripciones.html", form=form)