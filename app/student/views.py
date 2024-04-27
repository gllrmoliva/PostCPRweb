from . import student 
from flask import render_template, request, redirect, url_for, session

from login_required import login_required
from database import db

"""
Cosas basicas sobre la interfaz de Estudiante:
- En la barra de navegación superior, se debe poder: cerrar sesión, ir a la homepage(ver cual es la homepage),
Ir a la vision de cursos, ir a la vision de evaluaciones (probablemente tambien se deba añadir una vista para 
ver las evaluaciones dentro de cada curso, tipo seccion de evaluaciones INFODA)
"""

"""
Aquí se muestran los cursos a los que pertenece el estudiante, en esta pagina se debe poder:
- Entrar a los cursos a los que pertenece el estudiante
"""
@student.route("/", methods = ['GET', 'POST'])
@login_required('student')
def homestudent():

    # Accedemos a la base de datos
    database = db.Connection()
    database.connect()

    # Obtenemos el usuario a partir de la variable global session, guardamos datos de usuario anteriormente(auth)
    user = database.get_user(session['user_id'])
    # aqui tambien obtenemos los cursos del estudiante 
    courses = database.get_courses_from_student(user)

    if request.method == 'GET':
        # Renderizamos la plantilla de student home, y le pasamos los cursos sacados de la base de datos previamente
        return render_template('student/home.html',courses = courses)
    
    # El metodo post se esta usando para manejar que sucede cuando apretamos los botones de ingresar a curso
    if request.method == 'POST':
        # obtenemos los datos del formulario apretado
        request_form = request.form
        # si el formulario apretado tiene un input hidden del tipo course, entonces hacermos una acción
        if request_form['type'] == 'course':
            # si la acción de formulario es entrar al curso, entonces entramos
            if request_form['action'] == 'enter':
                #TODO: agregar vista de que se vera en el curso
                # por ahora es solo los datos del curso
                return str(database.get_course(request_form['id']))

"""
En esta pagina se muestran las tareas dentro de un curso seleccionado en la ruta homestudent,
ademas estas tareas muestran su fecha limite de entrega y estado. Las tareas son clickables y 
te llevan a la pagina de la tarea (ruta: task_student)
"""
@student.route("/c/<courseid>", methods = ['GET', 'POST'])
@login_required('student')
def coursestudent(courseid):
    if request.method == 'GET':
        return render_template('student/course.html', courseid = courseid)
    elif request.method == 'POST':
        request_form = request.form
        if request_form['type'] == 'course':
            if request_form['action'] == 'enter':
                #TODO: agregar vista de que se vera en el curso
                return "estas entrando a un curso"


"""
En esta ruta, se muestra la tarea del usuario. Aquí el usuario puede:
- Ver los datos de la tarea (nombre, descripcion, estado, deadline, etc)
- Si la tarea no ha sido entregada todavia debe dejar la opción de entregar.
- Si la tarea ya fue entregada se debe mostrar la entrega que hizo el estudiante.
- Si la tarea no fue entregada en el tiempo limite, debe mostrar de alguna forma que no se puede entregar
porque se excedio el tiempo limite.
"""
@student.route("/t/<taskid>", methods = ['GET', 'POST'])
@login_required('student')
def taskstudent(taskid):
    if request.method == 'GET':
        return render_template('student/uploadtask.html')
    elif request.method == 'POST':
        return render_template('algo')
