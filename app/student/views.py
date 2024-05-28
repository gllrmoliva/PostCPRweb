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
- En la barra de navegación superior, se debe poder: cerrar sesión, ir a la homepage (TODO: ver cual es la homepage),
Ir a la vision de cursos, ir a la vision de evaluaciones (probablemente tambien se deba añadir una vista para 
ver las evaluaciones dentro de cada curso, tipo seccion de evaluaciones INFODA)
"""

database = Database(engine)


@student.route("/", methods = ['GET'])
@login_required('student')
def home():
    user = database.get_user(session["user_id"])
    """
    Aquí se muestran los cursos a los que pertenece el estudiante, en esta pagina se debe:
    - Entrar a los cursos a los que pertenece el estudiante
    """

    # aqui tambien obtenemos los cursos del estudiante
    courses = database.get_courses_from_student(user)

    # Esto no estaba antes (gllrm)
    for course in courses:
        print(f"{course}")
        course.tutor_name = database.get_user(course.tutor_id).name
    
    return render_template("student/home.html", courses=courses)


@student.route("/c/<courseid>", methods = ['GET'])
@login_required('student')
def course(courseid):
    """
    En esta pagina se muestran las tareas dentro de un curso seleccionado en la ruta homestudent,
    ademas estas tareas muestran su fecha limite de entrega y estado. Las tareas son clickables y 
    te llevan a la pagina de la tarea (ruta: task_student)
    """

    student = database.get_user(session["user_id"])
    course = database.get_course(courseid)

    tasks = database.get_tasks_from_course(course)

    return render_template("student/course.html", course=course, tasks=tasks)

@student.route("/t/<task_id>", methods = ['GET'])
@login_required('student')
def task(task_id):
    """
    En esta ruta, se muestra la tarea del usuario. Aquí el usuario puede:
    - Ver los datos de la tarea (nombre, descripcion, estado, deadline, etc)
    - Si la tarea no ha sido entregada todavia debe dejar la opción de entregar.
    - Si la tarea ya fue entregada se debe mostrar la entrega que hizo el estudiante.
    - Si la tarea no fue entregada en el tiempo limite, debe mostrar de alguna forma que no se puede entregar
    porque se excedio el tiempo limite.
    """

    task = database.get_task(task_id)

    print(f"TASK: {task}")
    # Esto ahora mismo muestra distintas cosas dependiento del estado
    # estos son : entregado, no entregado, pendiente, evaluado
    return render_template('student/uploadtask.html', task = task,estado = "evaluado")


@student.route("/c/<courseid>", methods = ['POST'])
@login_required('student')
def course_post(courseid):

    # Accedemos a la base de datos
    student = database.get_user(session['user_id'])
    course = database.get_course(courseid)

    # puede que esta ruta no sea necesaria, ya que redirigimos a los cursos a traves de href en 
    # html
    return "se hizo una peticion post a coursetutor"




@student.route("/t/<task_id>", methods = ['POST'])
@login_required('student')
def task_post(task_id):
    """
    En esta ruta se manejara como se añadiran los datos que ofrecio el usuario en el formulario al 
    entregar la tarea a la base de datos.
    """

    return "metodo post en taskstudent"

@student.route("/reviews", methods = ['GET'])
@login_required('student')
def reviews():
    """
    En esta ruta se mostraran todas las tareas que deben ser evaluadas por un estudiante.
    aquí se muestra una tabla con distintos parametros: Curso,Nombre de tarea,descripción. En esta pestaña
    solo se mostraran las tareas que no se han revisado, luego de ser revisadas no mostraran al student.
    """

    return render_template('student/reviews.html') 


# La variable task id se va a entregar cuando se redirija desde otra pagina
@student.route("/review/t/<task_id>", methods = ['GET'])
@login_required('student')
def review_task(task_id):
    """
    En esta pagina se debe completar la evaluación de una tarea con respecto a los criterios establecidos
    por el tutor.
    """

    return render_template('student/reviewtask.html', task_id = task_id) 


@student.route("/review/t/<task_id>", methods = ['POST'])
@login_required('student')
def review_task_post(task_id):
    """
    Aquí se van a subir las respuestas dadas por el estudiante para la evaluación
    """
    request_form = request.form
    lista_keys = []
    lista_values= []

    for key, values in request_form.items():
        lista_keys.append(key)
        lista_values.append(values)

    return str(lista_keys) + "<hr>" + str(lista_values)