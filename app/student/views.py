from . import student
from flask import render_template, request, redirect, url_for, session, flash

from login_required import login_required
from database import db
from database.models import engine
from sqlalchemy.orm import sessionmaker
from database.models import *
from database.schemas import Database

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
database = Database(engine)


@student.route("/", methods=["GET", "POST"])
@login_required("student")
def homestudent():
    user = database.get_user(session["user_id"])

    # aqui tambien obtenemos los cursos del estudiante
    courses = database.get_courses_from_student(user)

    # Esto no estaba antes (gllrm)
    for course in courses:
        course.tutor_name = database.get_user(course.tutor_id).name
    # Si accedemos con el metodo get
    if request.method == "GET":
        # Renderizamos la plantilla de student home, y le pasamos los cursos sacados de la base de datos previamente
        return render_template("student/home.html", courses=courses)

    # El metodo post se esta usando para manejar que sucede cuando apretamos los botones de ingresar a curso
    if request.method == "POST":
        # obtenemos los datos del formulario apretado
        request_form = request.form
        # si el formulario apretado tiene un input hidden del tipo course, entonces hacermos una acción
        if request_form["type"] == "course":
            # si la acción de formulario es entrar al curso, entonces entramos
            if request_form["action"] == "enter":
                # TODO: agregar vista de que se vera en el curso
                # por ahora es solo los datos del curso
                return redirect(
                    url_for("student.coursestudent", courseid=int(request_form["id"]))
                )


"""
En esta pagina se muestran las tareas dentro de un curso seleccionado en la ruta homestudent,
ademas estas tareas muestran su fecha limite de entrega y estado. Las tareas son clickables y 
te llevan a la pagina de la tarea (ruta: task_student)
"""


@student.route("/c/<courseid>", methods=["GET", "POST"])
@login_required("student")
def coursestudent(courseid):

    student = database.get_user(session["user_id"])
    course = database.get_course(courseid)

    if request.method == "GET":
        tasks = database.get_tasks_from_course(course)
        return render_template("student/course.html", course=course, tasks=tasks)

    elif request.method == "POST":
        return "se hizo una peticion post a coursetutor"


"""
En esta ruta, se muestra la tarea del usuario. Aquí el usuario puede:
- Ver los datos de la tarea (nombre, descripcion, estado, deadline, etc)
- Si la tarea no ha sido entregada todavia debe dejar la opción de entregar.
- Si la tarea ya fue entregada se debe mostrar la entrega que hizo el estudiante.
- Si la tarea no fue entregada en el tiempo limite, debe mostrar de alguna forma que no se puede entregar
porque se excedio el tiempo limite.
"""


@student.route("/t/<task_id>", methods=["GET", "POST"])
@login_required("student")
def taskstudent(task_id):

    task = database.get_task(task_id)
    print(f"TASK: {task}")
    if request.method == "GET":
        return render_template("student/uploadtask.html", task=task)
    elif request.method == "POST":
        return "metodo post en taskstudent"
