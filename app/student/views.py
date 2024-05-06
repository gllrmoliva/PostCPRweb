from . import student 
from flask import render_template, request, redirect, url_for, session, flash

from login_required import login_required
from database import db

"""
Cosas basicas sobre la interfaz de Estudiante:
- En la barra de navegación superior, se debe poder: cerrar sesión, ir a la homepage (TODO: ver cual es la homepage),
Ir a la vision de cursos, ir a la vision de evaluaciones (probablemente tambien se deba añadir una vista para 
ver las evaluaciones dentro de cada curso, tipo seccion de evaluaciones INFODA)
"""

@student.route("/", methods = ['GET'])
@login_required('student')
def homestudent():
    """
    Aquí se muestran los cursos a los que pertenece el estudiante, en esta pagina se debe:
    - Entrar a los cursos a los que pertenece el estudiante
    """

    # Accedemos a la base de datos
    database = db.Connection()
    database.connect()

    # Obtenemos el usuario a partir de la variable global session, guardamos datos de usuario anteriormente(auth)
    user = database.get_user(session['user_id'])
    # aqui tambien obtenemos los cursos del estudiante 
    courses = database.get_courses_from_student(user)

    # Esto no estaba antes (gllrm)
    for course in courses:
        course['tutor_name'] = database.get_user(course['tutor_id'])['name']

    # Renderizamos la plantilla de student home, y le pasamos los cursos sacados de la base de datos previamente
    return render_template('student/home.html',courses = courses)


# Lo mas probable es que esto no sea necesario
@student.route("/", methods = ['POST'])
@login_required('student')
def homestudent_post():
    return "se uso post en home_student"


@student.route("/c/<courseid>", methods = ['GET'])
@login_required('student')
def coursestudent(courseid):
    """
    En esta pagina se muestran las tareas dentro de un curso seleccionado en la ruta homestudent,
    ademas estas tareas muestran su fecha limite de entrega y estado. Las tareas son clickables y 
    te llevan a la pagina de la tarea (ruta: task_student)
    """

    # Accedemos a la base de datos
    database = db.Connection()
    database.connect()

    student = database.get_user(session['user_id'])
    course = database.get_course(courseid)

    if (course in database.get_courses_from_student(student)):
        tasks = database.get_tasks_from_course(course)
        return render_template('student/course.html', course = course, tasks=tasks)
    else:
        flash('No se puede acceder a ese curso')
        return redirect(url_for('tutor.hometutor'))



@student.route("/c/<courseid>", methods = ['POST'])
@login_required('student')
def coursestudent_post(courseid):

    # Accedemos a la base de datos
    database = db.Connection()
    database.connect()

    student = database.get_user(session['user_id'])
    course = database.get_course(courseid)

    # puede que esta ruta no sea necesaria, ya que redirigimos a los cursos a traves de href en 
    # html
    return "se hizo una peticion post a coursetutor"


@student.route("/t/<task_id>", methods = ['GET'])
@login_required('student')
def taskstudent(task_id):
    """
    En esta ruta, se muestra la tarea del usuario. Aquí el usuario puede:
    - Ver los datos de la tarea (nombre, descripcion, estado, deadline, etc)
    - Si la tarea no ha sido entregada todavia debe dejar la opción de entregar.
    - Si la tarea ya fue entregada se debe mostrar la entrega que hizo el estudiante.
    - Si la tarea no fue entregada en el tiempo limite, debe mostrar de alguna forma que no se puede entregar
    porque se excedio el tiempo limite.
    """

    database = db.Connection()
    database.connect()

    task = database.get_task(task_id)

    return render_template('student/uploadtask.html', task = task)


@student.route("/t/<task_id>", methods = ['POST'])
@login_required('student')
def taskstudent_post(task_id):
    """
    En esta ruta se manejara como se añadiran los datos que ofrecio el usuario en el formulario al 
    entregar la tarea a la base de datos.
    """

    database = db.Connection()
    database.connect()

    task = database.get_task(task_id)

    return "metodo post en taskstudent"