from . import tutor
from flask import render_template, request, redirect, url_for, session, flash
from login_required import login_required
from database import db
import sqlite3
from database.models import engine
from sqlalchemy.orm import sessionmaker
from database.models import *
from database.functions import Database
from datetime import date

database = Database(engine)


@tutor.route("/", methods=["GET"])
@login_required("tutor")
def home():

    # Recuperamos de la base de datos el usuario, para luego recuperar los cursos
    user = database.get_user(session["user_id"])
    courses = database.get_courses_from_tutor(user)

    # A render_template le damos la variable courses, ya que jinja lo usa para mostrar los cursos del
    # usuario (ver tutor/home.html para ver como es utilizado courses)
    return render_template("tutor/home.html", courses=courses)


@tutor.route("/", methods=["POST"])
@login_required("tutor")
def home_post():

    # Recuperamos de la base de datos el usuario, para luego recuperar los cursos
    user = database.get_user(session["user_id"])

    # Obtenemos los datos del formulario
    request_form = request.form

    # Notemos que en tutor/home.html, los forms tienen 2 propiedades importantes name y value
    # para obtener los datos podemos hacer lo siguiente request.form['name'] = value
    # entonces:
    # - si form_type es create_course, intentamos crear el curso con el nombre dado. Si esto no funciona
    #   enviamos al usuario a home
    if request_form["form_type"] == "create_course":
        try:
            database.add_course(request_form["name"], user)
            return redirect(url_for("tutor.home"))

        except sqlite3.IntegrityError:
            flash("Ya existe un curso con ese nombre")
            return redirect(url_for("tutor.home"))
        except Exception as e:
            flash(e)
            return redirect(url_for("tutor.home"))


@tutor.route("/c/<int:courseid>", methods=["GET"])
@login_required("tutor")
def course(courseid):

    # Obtenemos al usuario(tutor) y el curso (con el id)
    tutor = database.get_user(session["user_id"])
    course = database.get_course(courseid)

    # Si el tutor pertenece al curso:
    # - se obtienen las tareas del curso y se renderiza la template tutor/course.html
    # Si el tutor no pertenece al curso:
    # - Se envia al usuario a home y se muestra una advertencia en pantalla (flash)
    tasks = database.get_tasks_from_course(course)
    return render_template("tutor/course.html", course=course, tasks=tasks)


@tutor.route("/c/<int:courseid>", methods=["POST"])
@login_required("tutor")
def course_post(courseid):

    course = database.get_course(courseid)
    request_form = request.form
    # Si se presiona el botón crear tarea:
    # - Se recuperan los datos del formulario.
    # - intentamos crear el curso, si no se puede, se muestra el error en pantalla
    if request_form["form_type"] == "create_task":

        name = request_form["name"]
        instructions = request_form["instructions"]
        date = request_form["date"]
        deadline = request_form["deadline"]
        #TODO: al crear una tarea se debe añadir una fecha de entrega y una fecha limite de revision
        # El formato de estas es: YYYY-MM-DD
        database.create_task(name, instructions, course)

        return redirect(url_for("tutor.course", courseid=courseid))

    return "se hizo una peticion post a course (tutor): " + str(request_form)


@tutor.route("/c/<int:courseid>/edit", methods=["GET"])
@login_required("tutor")
def editcourse(courseid):

    tutor = database.get_user(session["user_id"])
    course = database.get_course(courseid)
    # TODO una función que me los datos de los alumnos dentro de un curso, tienen que ser los datos 
    # guardados dentro de Usuario (nombre, id, correo, etc)
    return render_template("tutor/editcourse.html", course = course)

@tutor.route("/c/<int:courseid>/edit", methods=["POST"])
@login_required("tutor")
def editcourse_post(courseid):

    tutor = database.get_user(session["user_id"])
    course = database.get_course(courseid)

    request_form = request.form

    if request_form["form_type"] == "add_student":

        email = request_form["email"]
        # TODO: Aquí deberia exitir una función que añada un usuario a un curso, si el usuario existe 
        # dentro de la DB, que lo añada y retorne true, si no existe que retorne False. Esto para más adelante 
        # tirar un error si no se pudo añadir al usuario porque no existe. Notar que a un usuario no se le 
        # puede añadir dos veces al mismo curso y que cuando se añade un usuario cuando ya hay tareas creadas, al
        # nuevo usuario se le deben agregar las tarea del curso. Esto igualmente podria crear errores si la tarea ya tiene un 
        # tiempo limite, igualmente ver :)
        flash("DEBUG: Se agrego un nuevo usuario")
        return redirect(url_for("tutor.editcourse", courseid=courseid))

    elif request_form["form_type"] == "delete_student":
        email = request_form["email"]
        # TODO: Aquí borrar al usuario del curso y todo lo relacionado entremedio

        flash(f"DEBUG: El usuario {email} se ha eliminado del curso")
        return redirect(url_for("tutor.editcourse", courseid=courseid))

    elif request_form["form_type"] == "edit_course_name":
        # TODO: Aquí se deberia cambiar el nombre del curso, dentro de la DB 
        # Manejar cuando hayan dos cursos con nombre igual¿? y cuando se ponga el mismo nombre al curso otra vez

        new_name = request_form["course_name"]

        flash(f"DEBUG: el curso ha cambiado de nombre a {new_name}")
        return redirect(url_for("tutor.editcourse", courseid=courseid))

    return "se hizo una péticion post en editcourse y paso algo raro: " + str(request_form)



@tutor.route("c/<course_id>/t/<task_id>", methods=["GET"])
@login_required("tutor")
def task(course_id, task_id):
    # Obtenemos la tarea y los criterios de la tarea
    # TODO ¿Agregar un campo Descripción a tabla Criterion?
    task = database.get_task(task_id)
    criteria = database.get_criteria_from_task(task)
    submissions = database.get_submissions_from_task(task)
    print(f"TASK: {task}")
    data = []

    for submission in submissions:
        name = database.get_name_from_student(submission.student_id)
        review_id = database.get_review_by_submission(
            submission.submission_id, user_id=session["user_id"]
        ).review_id
        review = database.get_review(review_id)
        data.append((review_id, review, submission, name))

    course = database.get_course(course_id=course_id)

    return render_template(
        "tutor/tasktutor.html", course=course, task=task, criteria=criteria, data=data
    )

@tutor.route("/post/t/", methods=["POST"])
@login_required("tutor")
# TODO hacer esta ruta
def task_post():
    form = request.form
    if form['action'] == 'calculate_grades':
        # Agregar aquí función que calcula las notas con el algoritmo
        flash(f"DEBUG: Las notas han sido calculadas {str(form)}")
        pass
    return redirect(url_for('tutor.task', course_id = form['course_id'], task_id = form['task_id']))



# Necesita método POST para modificar tasks existentes supongo?
@tutor.route("c/<course_id>/t/<task_id>/edit", methods=["GET"])
@login_required("tutor")
def edit_task(course_id, task_id):
    # Obtenemos la tarea y los criterios de la tarea
    task = database.get_task(task_id)
    criteria = database.get_criteria_from_task(task)
    
    return render_template("tutor/tasktutor_edit.html", task=task, criteria=criteria)

@tutor.route("c/<course_id>/t/<task_id>/edit", methods=["POST"])
@login_required("tutor")
def edit_task_post(course_id, task_id):
    return request.form



@tutor.route("c/<course_id>/t/<task_id>/r/<review_id>", methods=["GET"])
@login_required("tutor")
def submission(course_id, task_id, review_id):

    task = database.get_task(task_id)
    submission = database.get_submission_by_review(review_id)
    course = database.get_course(course_id=course_id)
    criteria = database.get_criteria_from_task(task)

    if database.is_review_reviewed(review_id, session["user_id"]) is True:
        data = []
        flash("Esa entrega ya ha sido evaluada")
        return redirect(url_for("tutor.task",course_id=course_id,task_id = task_id))

    return render_template(
        "tutor/review.html",
        task=task,
        review_id=review_id,
        submission=submission,
        course=course,
        criteria=criteria,
    )


@tutor.route("c/<course_id>/t/<task_id>/r/<review_id>", methods=["POST"])
@login_required("tutor")
def review_post(course_id, task_id, review_id):
    request_form = request.form

    # Información para lógica del endpoint
    date1 = date.today()
    submission = database.get_submission_by_review(review_id)
    user_id = session["user_id"]
    database.mark_review_as_reviewed(submission=submission, user_id=user_id)
    print(f"request form: {request_form}")
    teacher_score = 0

    for criterion_name, score in request_form.items():
        criterion = database.get_criterion_by_name(criterion_name, task_id)
        database.create_review_criterion(review_id, criterion.criterion_id, score)
        teacher_score += int(score)
    database.mark_submission_as_reviewed(
        submission=submission, date=date1, teacher_score=teacher_score
    )

    return redirect(url_for("tutor.task", course_id=course_id, task_id=task_id))
