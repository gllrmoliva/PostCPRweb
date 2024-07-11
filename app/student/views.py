from . import student
from flask import render_template, request, redirect, url_for, session, flash

from login_required import login_required
from sqlalchemy.orm import sessionmaker
from database.model import *
from database.studentdatabase import StudentDatabase
from datetime import date

"""
Cosas basicas sobre la interfaz de Estudiante:
- En la barra de navegación superior, se debe poder: cerrar sesión, ir a la homepage (TODO: ver cual es la homepage),
Ir a la vision de cursos, ir a la vision de evaluaciones (probablemente tambien se deba añadir una vista para 
ver las evaluaciones dentro de cada curso, tipo seccion de evaluaciones INFODA)
"""

database = StudentDatabase()
database.init()

@student.route("/", methods=["GET"])
@login_required("STUDENT")
def home():
    """
    Aquí se muestran los cursos a los que pertenece el estudiante, en esta pagina se debe:
    - Entrar a los cursos a los que pertenece el estudiante
    """

    student = database.set_student(session["user_id"])

    return render_template("student/home.html", courses=student.courses)


@student.route("/c/<course_id>", methods=["GET"])
@login_required("STUDENT")
def course(course_id):
    """
    En esta pagina se muestran las tareas dentro de un curso seleccionado en la ruta homestudent,
    ademas estas tareas muestran su fecha limite de entrega y estado. Las tareas son clickables y
    te llevan a la pagina de la tarea (ruta: task_student)
    """

    student = database.set_student(session["user_id"])
    course = database.get_from_id(Course, course_id)

    return render_template("student/course.html",
                           course=course,
                           task_completion_status=database.task_completion_status)


@student.route("/t/<task_id>", methods=["GET"])
@login_required("STUDENT")
def task(task_id):
    """
    En esta ruta, se muestra la tarea del usuario. Aquí el usuario puede:
    - Ver los datos de la tarea (nombre, descripcion, estado, deadline, etc)
    - Si la tarea no ha sido entregada todavia debe dejar la opción de entregar.
    - Si la tarea ya fue entregada se debe mostrar la entrega que hizo el estudiante.
    - Si la tarea no fue entregada en el tiempo limite, debe mostrar de alguna forma que no se puede entregar
    porque se excedio el tiempo limite.
    """

    student = database.set_student(session["user_id"])
    task = database.get_from_id(Task, task_id)
    state = database.task_completion_status(task)
    submission = database.get_submission(task)
    criteria = task.criteria

    # TODO : Los siguientes estados: 
    # REVISADO
    return render_template("student/uploadtask.html",
                           task=task,
                           submission=submission,
                           estado=state,
                           task_max_score=database.task_max_score(task),
                           criteria = criteria)



@student.route("/c/<course_id>", methods=["POST"])
@login_required("STUDENT")
def course_post(course_id):

    # ¿cuando accedemos a aca?? - mati
    print("Holaaaaaaaaaaaaaaa!!!")

    # puede que esta ruta no sea necesaria, ya que redirigimos a los cursos a traves de href en
    # html
    return "se hizo una peticion post a coursetutor"


@student.route("/t/<task_id>", methods=["POST"])
@login_required("STUDENT")
def task_post(task_id):
    """
    En esta ruta se manejara como se añadiran los datos que ofrecio el usuario en el formulario al
    entregar la tarea a la base de datos.
    """

    # Obtenemos las variables a usar
    student = database.set_student(session["user_id"])
    task = database.get_from_id(Task, task_id)
    request_form = request.form
    submission_url = request_form['submission_url']

    # Ingresamos la tarea a la base de datos
    new_submission = Submission(url=submission_url, student=student, task=task) # TODO: añadir fecha
    database.add(new_submission)
    database.commit_changes()

    flash("Tarea entregada exitosamente.")
    return redirect(url_for('student.course', course_id=task.course.id))


@student.route("/reviews", methods=["GET"])
@login_required("STUDENT")
def reviews():
    reviews_to_review = database.get_reviews_to_review(session["user_id"])
    tasks_to_review = database.get_tasks_to_review(reviews_to_review)
    data = []
    for i in range(len(reviews_to_review)):
        data.append(
            (
                reviews_to_review[i],
                tasks_to_review[i],
                database.get_course(tasks_to_review[i].course_id),
            )
        )

    return render_template("student/reviews.html", data=data)


# La variable task id se va a entregar cuando se redirija desde otra pagina
@student.route("/review/t/<task_id>/r/<review_id>", methods=["GET"])
@login_required("STUDENT")
def review_task(review_id, task_id):
    if database.is_review_reviewed(review_id, session["user_id"]) is True:
        flash("Esa entrega ya ha sido evaluada")
        return redirect(url_for("student.reviews"))
    criteria = database.get_all_criteria_from_task(task_id)
    task_to_show = database.get_task(task_id)
    review = database.get_review(review_id)
    submission = database.get_submission_by_review(review_id)
    return render_template(
        "student/reviewtask.html",
        task=task_to_show,
        criteria=criteria,
        review=review,
        submission=submission,
    )


@student.route("/review/t/<task_id>/r/<review_id>", methods=["POST"])
@login_required("STUDENT")
def review_task_post(task_id, review_id):
    """
    Aquí se van a subir las respuestas dadas por el estudiante para la evaluación
    """
    date1 = date.today()
    submission = database.get_submission_by_review(review_id)
    user_id = session["user_id"]
    database.mark_review_as_reviewed(submission=submission, user_id=user_id)
    request_form = request.form
    print(f"request form: {request_form}")
    for criterion_name, score in request_form.items():
        criterion = database.get_criterion_by_name(criterion_name, task_id)
        database.create_review_criterion(review_id, criterion.criterion_id, score)
    return redirect(url_for("student.reviews"))
