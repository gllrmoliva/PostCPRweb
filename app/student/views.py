from . import student
from flask import render_template, request, redirect, url_for, session, flash

from login_required import login_required
from database.model import *
from database.student_database import StudentDatabase

"""
Cosas basicas sobre la interfaz de Estudiante:
- En la barra de navegación superior, se debe poder: cerrar sesión, ir a la homepage,
Ir a la vision de cursos, ir a la vision de calificaciones 
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

    # Es necesario vincular el estudiante a la base de datos en cada ruta
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

    if student in course.students:
        return render_template("student/course.html",
                            course=course,
                            task_completion_status=database.task_completion_status)
    else:
        flash("No perteneces a este curso")
        return redirect(url_for("student.home"))



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

    # TODO : Los siguientes estados: 
    # REVISADO
    if student in task.course.students:
        return render_template("student/uploadtask.html",
                            task=task,
                            submission=submission,
                            estado=state,
                            task_max_score=database.task_max_score(task),
                            criterion_score=database.criterion_tutor_score,
                            task_score=database.task_tutor_score(task))
    else:
        flash("No perteneces a este curso")
        return redirect(url_for("student.home"))

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
    """
        Aquí se muestran las tareas que un estudiante debe revisar, solo se muestran las 
        estan pendientes de revisión. 
    """
    # Obtenemos las variables a usar
    student = database.set_student(session["user_id"])

    return render_template("student/reviews.html", reviews=student.reviews)


# La variable task id se va a entregar cuando se redirija desde otra pagina
@student.route("/review/r/<review_id>", methods=["GET"])
@login_required("STUDENT")
def review_task(review_id):
    """
    Accedemos a la revisión de la tarea con el id review_id
    """

    # Obtenemos las variables a usar
    student = database.set_student(session["user_id"])
    review = database.get_from_id(Review, review_id)

    if not review.is_pending:
        flash("Esta entrega ya ha sido evaluada")
        return redirect(url_for("student.reviews"))
    elif review.submission.task.state == "COMPLETED":
        flash("Esta tarea ya no acepta más revisiones")
        return redirect(url_for("student.reviews"))

    if review.reviewer == student:
        return render_template(
            "student/reviewtask.html",
            review=review,
        )
    else:
        flash("No tienes permisos para acceder a esta ruta.")
        return render_template("student/reviews.html", reviews=student.reviews)


@student.route("/review/r/<review_id>", methods=["POST"])
@login_required("STUDENT")
def review_task_post(review_id):
    """
    Aquí se suben las respuestas dadas por el estudiante para una evaluación.
    """

    # Obtenemos las variables a usar
    student = database.set_student(session["user_id"])
    review = database.get_from_id(Review, review_id)
    request_form = request.form   
    # date1 = date.today()

    # Creamos la revisión de cada criterio
    criterion_review_list = []

    for criterion in review.submission.task.criteria:
        if str(criterion.id) in request_form:
            # Corresponde al valor entregado en el request, va desde 0 a 1 siempre
            input_score = float(request_form[str(criterion.id)]) # El diccionario tiene valores en formato string

            actual_score = input_score * criterion.max_score

            # Creamos la revisión del criterio actual
            criterion_review = CriterionReview(review=review, criterion=criterion, score=actual_score)
            criterion_review_list.append(criterion_review)

        else:   # Idealmente nunca se deberia llegar a esta parte del codigo
            flash("Es necesario evaluar todos los criterios de la tarea")
            return redirect(url_for('student.review_task', review_id=review_id))
    
    database.add_all(criterion_review_list)
    review.is_pending = False
    database.commit_changes()
    flash("Revision enviada exitosamente")

    return redirect(url_for("student.reviews"))

# TODO
@student.route("/grades", methods=["GET"])
@login_required("STUDENT")
def grades():
    """
    En esta vista se muestran las calificaciones obtenidas por un estudiante en todos los cursos en los que 
    participa.
    """

    student = database.set_student(session["user_id"])

    return render_template("student/grades.html", student = student
                                                , task_completion_status = database.task_completion_status
                                                , task_score = database.task_tutor_score
                                                , task_max_score = database.task_max_score)
