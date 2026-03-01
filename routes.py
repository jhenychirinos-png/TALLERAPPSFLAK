from app import app, db
from flask import render_template,request,redirect,url_for
import formularios
from models import Tarea

@app.route('/')
@app.route('/index')
def index():
        return render_template('index.html', subtitulo = "Actidad en grupo TAI")

@app.route('/sobrenosotros', methods = ['GET', 'POST'])
def sobrenosotros():
        formulario = formularios.FormAgregarTareas()
        tareas = Tarea.query.all()  
        if formulario.validate_on_submit() :
                nueva_tarea = Tarea (titulo =  formulario.titulo.data)
                db.session.add(nueva_tarea)
                db.session.commit()
                print('se envio correctamente', formulario.titulo.data)
                return render_template('sobrenosotros.html', 
                                       form = formulario,
                                       titulo = formulario.titulo.data,
                                       tareas = tareas)
                                        
        return render_template('sobrenosotros.html', form = formulario,tareas = tareas)
    
@app.route('/saludo')
def saludo():
        return 'Hola bienvenido a Taller Apps '
    
@app.route('/usuario/<nombre>')
def usuario(nombre):
        return f'Hola{nombre} bienvenido a Taller Apps '

@app.route('/eliminar/<int:id>')
def eliminar(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for('sobrenosotros'))  # Redirige a sobrenosotros

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    tarea = Tarea.query.get_or_404(id)
    formulario = formularios.FormAgregarTareas(obj=tarea) # Inicializa el formulario con la tarea existente
    if formulario.validate_on_submit():
        tarea.titulo = formulario.titulo.data
        db.session.commit()
        return redirect(url_for('sobrenosotros'))  # Redirige a sobrenosotros
    return render_template('editar.html', form=formulario, tarea=tarea) # Pasa el formulario y la tarea al template