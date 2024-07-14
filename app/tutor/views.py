from . import tutor
from flask import render_template, request, redirect, url_for, session, flash

from login_required import login_required
from database.model import *
from database.database import IntegrityException
from database.tutor_database import TutorDatabase
from database.time import Time

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

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    course = database.get_from_id(Course, course_id)
    request_form = request.form

    # Si se presiona el botón crear tarea:
    # - Se recuperan los datos del formulario.
    # - intentamos crear el curso, si no se puede, se muestra el error en pantalla
    if request_form["form_type"] == "create_task":

        # Creamos la nueva tarea con las variables entregas en el formulario
        task = Task(
            name = request_form["name"],
            instructions = request_form["instructions"],
            deadline_date = Time.string_to_object(request_form["deadline_date"]),
            review_deadline_date = Time.string_to_object(request_form["review_deadline_date"]),

            course = course,
        )

        database.add(task)
        database.commit_changes()

        return redirect(url_for("tutor.course", course_id=course_id))

    # No se deberia llegar nunca a esta linea
    return "se hizo una peticion post a course (tutor): " + str(request_form)


@tutor.route("/c/<course_id>/edit", methods=["GET"])
@login_required("TUTOR")
def editcourse(course_id):

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    course = database.get_from_id(Course, course_id)

    return render_template("tutor/editcourse.html", course=course)


@tutor.route("/c/<course_id>/edit", methods=["POST"])
@login_required("TUTOR")
def editcourse_post(course_id):

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    course = database.get_from_id(Course, course_id)
    request_form = request.form

    # En caso de que se esta solicitando añadir un estudiante
    if request_form["form_type"] == "add_student":

        student = database.get_student_from_email(request_form["email"])

        # Estudiante no existe
        if (student == None):
            flash("No existe estudiante con el correo dado")
            return redirect(url_for("tutor.editcourse", course_id=course_id))
        # Estudiante ya está en el curso:
        if (student in course.students):
            flash("El estudiante ya pertenece al curso")
            return redirect(url_for("tutor.editcourse", course_id=course_id))
        
        course.students.append(student)
        database.commit_changes()
        flash("Estudiante añadido satisfactoriamente")

        return redirect(url_for("tutor.editcourse", course_id=course_id))

    elif request_form["form_type"] == "delete_student":
        email = request_form["email"]
        # TODO: Aquí borrar al usuario del curso y todo lo relacionado entremedio

        flash(f"DEBUG: El usuario {email} se ha eliminado del curso")
        return redirect(url_for("tutor.editcourse", courseid=course_id))

    elif request_form["form_type"] == "edit_course_name":

        try:
            new_name = request_form["course_name"]
            course.name = new_name
            database.commit_changes()
            flash("Nombre del curso cambiado exitosamente")
            return redirect(url_for("tutor.editcourse", course_id=course_id))
        
        except IntegrityException:
            flash("Ya existe un curso de mismo nombre")
            database.rollback_changes()
            return redirect(url_for("tutor.editcourse", course_id=course_id))
        
        except Exception as e:  # Idealmente no se deberia llegar acá
            flash(e)
            return redirect(url_for("tutor.editcourse", course_id=course_id))

    return "se hizo una péticion post en editcourse y paso algo raro: " + str(request_form)



@tutor.route("/t/<task_id>", methods=["GET"])
@login_required("TUTOR")
def task(task_id):

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    task = database.get_from_id(Task, task_id)

    return render_template("tutor/tasktutor.html", task=task
                                                 , task_max_score = database.task_max_score(task)
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
@tutor.route("/t/<task_id>/edit", methods=["GET"])
@login_required("TUTOR")
def edit_task(task_id):

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    task = database.get_from_id(Task, task_id)
    
    return render_template("tutor/tasktutor_edit.html", task=task)

@tutor.route("/t/<task_id>/edit", methods=["POST"])
@login_required("TUTOR")
def edit_task_post(task_id): 

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    task = database.get_from_id(Task, task_id)

    # Hay cambios que son drásticos y que requieren desechar las revisiones hechas a la entrega
    major_changes = False

    # Actualizamos los datos de la tarea a partir del formulario
    task.name = request.form.get('name')
    task.instructions = request.form.get('instructions')
    task.deadline_date = Time.string_to_object(request.form.get('deadline_date'))
    task.review_deadline_date = Time.string_to_object(request.form.get('review_deadline_date'))
    
    # Editar los criterios existentes
    for criterion in task.criteria:

        # Eliminar criterio
        if request.form.get(f'delete_criterion_{criterion.id}') == "1":

            database.delete(criterion)
            major_changes = True

        # Modificar criterio
        else:
            criterion.name = request.form.get(f'criterion_name_{criterion.id}')
            criterion.description = request.form.get(f'criterion_description_{criterion.id}')

            new_max_score = float(request.form.get(f'criterion_max_score_{criterion.id}'))
            if (criterion.max_score != new_max_score):

                criterion.max_score = new_max_score
                major_changes = True

    # Crear nuevos criterios
    new_criterion_names = request.form.getlist('new_criterion_name[]')
    new_criterion_descriptions = request.form.getlist('new_criterion_description[]')
    new_criterion_max_scores = request.form.getlist('new_criterion_max_score[]')
    data = zip(new_criterion_names, new_criterion_descriptions, new_criterion_max_scores)

    for name, description, max_score in data:

        major_changes = True
        
        if name and description and max_score:  # Asegurarse de que no estén vacíos
            new_criterion = Criterion(name = name, description = description, max_score = max_score, task = task)
            task.criteria.append(criterion)

        else:
            flash("Se ingresaron parametros vacios al intentar creas nuevos criterios")
    
    # En caso de haberse hecho cambios mayores
    if (major_changes):
        # Eliminamos todas las revisiones obsoletas
        for submission in task.submissions:
            database.delete_all(submission.reviews)
    
    database.commit_changes()

    if (major_changes):
        flash("Se modificó la tarea exitosamente. Se desecharon las revisiones obsoletas")
    else:
        flash("Se modificó la tarea exitosamente")

    return redirect(url_for("tutor.course", course_id=task.course.id))



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
