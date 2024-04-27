from . import student 
from flask import render_template, request, redirect, url_for

from login_required import login_required
from database import db

import fakedatabase

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
    # Basicamente pareciese que siempre te tienes que conectar a una base de datos desde las rutas, y despues
    # trabajar con los metodos de la clase Connection, supongo que esta bien :)
    c = db.Connection()
    c.connect()

    # Aqui se esta creando un usuario, esto lo hay que borrar por ahora
    c.add_user("johnny@mail.com", "1234", "Johnny")
    user = c.get_user_from_email("johnny@mail.com")
    c.promote_to_student(user)

    request_form = request.form
    if request.method == 'GET':
        # Claramente el Cursos, debe ser sacado con una función de backend la cual de de output los cursos, con sus caracteristicas
        return render_template('student/home.html',cursos = fakedatabase.get_cursos())
    if request.method == 'POST':
        request_form = request.form
        if request_form['type'] == 'course':
            if request_form['action'] == 'enter':
                #TODO: agregar vista de que se vera en el curso
                return str(user)

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
