from . import tutor
from flask import render_template, request, redirect, url_for, session, flash

from login_required import login_required
from database.model import *
from database.database import IntegrityException
from database.tutor_database import TutorDatabase
from datetime import date

#import sqllite3    Se utilizaba para manejar excepciones, pero creo que importar un DBMS en frontend no es buena idea

database = TutorDatabase()
database.init()

@tutor.route("/", methods=["GET"])
@login_required("TUTOR")
def home():

    # Es necesario vincular el tutor a la base de datos en cada ruta
    tutor = database.set_tutor(session["user_id"])

    # A render_template le damos la variable courses, ya que jinja lo usa para mostrar los cursos del
    # usuario (ver tutor/home.html para ver como es utilizado courses)
    return render_template("tutor/home.html", courses=tutor.courses)


@tutor.route("/", methods=["POST"])
@login_required("TUTOR")
def home_post():

    tutor = database.set_tutor(session["user_id"])

    # Obtenemos los datos del formulario
    request_form = request.form

    # Notemos que en tutor/home.html, los forms tienen 2 propiedades importantes name y value
    # para obtener los datos podemos hacer lo siguiente request.form['name'] = value
    # entonces:
    # - si form_type es create_course, intentamos crear el curso con el nombre dado. Si esto no funciona
    #   enviamos al usuario a home
    if request_form["form_type"] == "create_course":

        try:
            new_course = Course(name = request_form["name"], tutor = tutor)
            database.add(new_course)
            database.commit_changes()
            return redirect(url_for("tutor.home"))
        
        except IntegrityException:
            flash("Ya existe un curso de mismo nombre")
            database.rollback_changes()
            return redirect(url_for("tutor.home"))
        
        except Exception as e:  # Idealmente no se deberia llegar acá
            flash(e)
            return redirect(url_for("tutor.home"))


@tutor.route("/c/<course_id>", methods=["GET"])
@login_required("TUTOR")
def course(course_id):

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    course = database.get_from_id(Course, course_id)

    # TODO Verificar que el tutor de la sesión es efectivamente el tutor del curso

    return render_template("tutor/course.html", course=course)


@tutor.route("/c/<course_id>", methods=["POST"])
@login_required("TUTOR")
def course_post(course_id):

    course = database.get_course(course_id)
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
        return redirect(url_for("tutor.course", course_id=course_id))

    return "se hizo una peticion post a course (tutor): " + str(request_form)


@tutor.route("/c/<course_id>/edit", methods=["GET"])
@login_required("TUTOR")
def editcourse(course_id):

    tutor = database.get_user(session["user_id"])
    course = database.get_course(course_id)

    return render_template("tutor/editcourse.html")


@tutor.route("/c/<course_id>/edit", methods=["POST"])
@login_required("TUTOR")
def editcourse_post(course_id):

    tutor = database.get_user(session["user_id"])
    course = database.get_course(course_id)

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
        return redirect(url_for("tutor.editcourse", courseid=course_id))

    elif request_form["form_type"] == "delete_student":
        email = request_form["email"]
        # TODO: Aquí borrar al usuario del curso y todo lo relacionado entremedio

        flash(f"DEBUG: El usuario {email} se ha eliminado del curso")
        return redirect(url_for("tutor.editcourse", courseid=course_id))

    elif request_form["form_type"] == "edit_course_name":
        # TODO: Aquí se deberia cambiar el nombre del curso, dentro de la DB 
        # Manejar cuando hayan dos cursos con nombre igual¿? y cuando se ponga el mismo nombre al curso otra vez

        new_name = request_form["course_name"]

        flash(f"DEBUG: el curso ha cambiado de nombre a {new_name}")
        return redirect(url_for("tutor.editcourse", courseid=course_id))

    return "se hizo una péticion post en editcourse y paso algo raro: " + str(request_form)



@tutor.route("c/<course_id>/t/<task_id>", methods=["GET"])
@login_required("TUTOR")
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
@login_required("TUTOR")
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
@login_required("TUTOR")
def edit_task(course_id, task_id):
    # Obtenemos la tarea y los criterios de la tarea
    task = database.get_task(task_id)
    criteria = database.get_criteria_from_task(task)
    
    return render_template("tutor/tasktutor_edit.html",task=task, criteria=criteria)

@tutor.route("c/<course_id>/t/<task_id>/edit", methods=["POST"])
@login_required("TUTOR")
def edit_task_post(course_id, task_id): 

    lista_debug = []
        # Obtener los datos del formulario
    task_name = request.form.get('task_name')
    task_instructions = request.form.get('task_instructions')
    deadline_date = request.form.get('deadline_date')
    review_deadline_date = request.form.get('review_deadline_date')

    # Recuperamos los criterios que hay en la tarea
    task = database.get_task(task_id)
    criteria = database.get_criteria_from_task(task)

    # Editar los criterios existentes
    for criterion in criteria:
        if request.form.get(f'delete_criterion_{criterion.criterion_id}') == "1":
            # AQUI SE DEBERIA ELIMINAR EL CRITERIO DE LA BASE DE DATOS
            pass
        else:
            criterion_name = request.form.get(f'criterion_name_{criterion.criterion_id}')
            criterion_description = request.form.get(f'criterion_description_{criterion.criterion_id}')
            lista_debug.append([criterion_name,criterion_description])
            # Actualizar el criterio en la base de datos
            # Aquí actualizar en base de datos
    
    # Crear nuevos criterios
    new_criterion_names = request.form.getlist('new_criterion_name[]')
    new_criterion_descriptions = request.form.getlist('new_criterion_description[]')

    for name, description in zip(new_criterion_names, new_criterion_descriptions):
        if name and description:  # Asegurarse de que no estén vacíos
            lista_debug.append([name,description])
            # Aqui crear criterio en base de datos
            pass
    
    return f"Los criterios ahora son: {str(lista_debug)}"


@tutor.route("/c/<course_id>/t/<task_id>/submissions", methods=["GET"])
@login_required("TUTOR")
def task_submissions(course_id, task_id):
    # Aquí necesitamos a los estudiantes de un curso, los puntajes obtenidos en la tarea, 
    return render_template("tutor/task_submissions.html",
                           course_id = course_id,
                           task_id= task_id) 


@tutor.route("/c/<course_id>/t/<task_id>/s/<submission_id>", methods=["POST"])
@login_required("TUTOR")
def task_submissions_post(course_id, task_id, submission_id):

    form = request.form
    if "accept" in form:
        flash("Se acepto wuaaat")
    elif "accept_all" in form:
        flash("Se acepto TODO wuuaaaaat")
    elif "review" in form:
        flash("Se review wuaaaat")
    # Esto de aca abajo es provicional uwu
    return redirect(url_for('tutor.task_submissions',
                     course_id = course_id, 
                     task_id = task_id))

@tutor.route("c/<course_id>/t/<task_id>/r/<review_id>", methods=["GET"])
@login_required("TUTOR")
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
@login_required("TUTOR")
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
