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
    """En esta vista se muestran todos los cursos que son de un tutor. Además, desde aquí se pueden 
    crear vistas nuevas.
    """
    # Es necesario vincular el tutor a la base de datos en cada ruta
    tutor = database.set_tutor(session["user_id"])

    # A render_template le damos la variable courses, ya que jinja lo usa para mostrar los cursos del
    # usuario (ver tutor/home.html para ver como es utilizado courses)
    return render_template("tutor/home.html", courses=tutor.courses)


@tutor.route("/", methods=["POST"])
@login_required("TUTOR")
def home_post():
    """
    Si el tutor presiono sobre el botón de crear curso y aceptar, el curso es creado.
    """
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
    """
    Se muestran las tareas disponible que tiene un curso sobre los cuales se puede presionar
    para acceder a ellos, además el tutor puede crear nuevas tareas.
    """
    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    course = database.get_from_id(Course, course_id)

    # TODO Verificar que el tutor de la sesión es efectivamente el tutor del curso

    return render_template("tutor/course.html", course=course)


@tutor.route("/c/<course_id>", methods=["POST"])
@login_required("TUTOR")
def course_post(course_id):
    """
    Si el tutor quiere crear una tarea, en esta ruta la tarea se crea y se commitea en la base de datos
    """

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
    """
    Ruta para editar un curso, se pueden añadir/eliminar estudiantes y cambiar el nombre del curso.
    TODO: Añadir posibilidad de eliminar curso
    """

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    course = database.get_from_id(Course, course_id)

    return render_template("tutor/editcourse.html", course=course)


@tutor.route("/c/<course_id>/edit", methods=["POST"])
@login_required("TUTOR")
def editcourse_post(course_id):
    """
    Recupera el formulario con los cambios hechos en la ruta editcourse y los commitea a 
    la base de datos si es posible.
    """

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

        student = database.get_student_from_email(request_form["email"])
        
        # Para eliminar un estudiante de un curso se debe:
        #   1. Quitar al estudiante del curso
        #   2. Eliminar las revisiones de dicho curso que ha hecho el estudiante
        #   3. Eliminar las entregas de dicho curso que ha hecho el estudiante
        #   3.1. Elimninar las revisiones de cada una de estas entregas
        
        # (2)
        for review in student.reviews:
            if review.submission.task.course == course:
                database.delete(review)
        
        # (3) y (3.1)
        for submission in student.submissions:
            if submission.task.course == course:
                database.delete_all(submission.reviews) # (3.1)
                database.delete(submission)
        
        # (1)
        course.students.remove(student)

        database.commit_changes()
        flash("Se ha removido al estudiante del curso exitosamente")

        return redirect(url_for("tutor.editcourse", course_id=course_id))

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
    """
    Es la vista de una sola tarea, en esta de muestran:
    - Nombre de la tarea
    - Descripción
    - Puntaje máximo
    - Fechas limite
    - Entregas hechas por alumno
    Además el tutor puede:
    - Eliminar tareas hechas por estudiantes
    - Editar la tarea
    - Asignar revisiones a los estudiantes (PCPR)
    """

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
    """
    Dependiendo de los botones presionados por el tutor en vista task, se ejecutan dos acciones:
    1. Eliminar una submission hecha por un alumno, esto le deja la posibilidad de enviarla nuevamente.
    2. Asignar revisiones a los alumnos dependiendo de las submission en el sistema.
    """
    
    form = request.form
    if 'delete_submission' in form:
        # Agregar aquí función que calcula las notas con el algoritmo
        flash(f"DEBUG: se ha borrado una submission {str(form)}")
    elif 'assign_reviews' in form:
        flash("Se asignaron las revisiones o el minimo de revisiones entregas debe ser 3¿?")
    return redirect(url_for('tutor.task', task_id = form['task_id']))


# Necesita método POST para modificar tasks existentes supongo?
@tutor.route("/t/<task_id>/edit", methods=["GET"])
@login_required("TUTOR")
def edit_task(task_id):
    """
    Vista para editar una tarea. En esta se puede:
    Agregar criterios, cambiar nombre de tarea, cambiar descripción de tarea.
    """

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    task = database.get_from_id(Task, task_id)
    
    return render_template("tutor/tasktutor_edit.html", task=task)

@tutor.route("/t/<task_id>/edit", methods=["POST"])
@login_required("TUTOR")
def edit_task_post(task_id): 
    """
    Aquí se ejecutan los cambios hechos por el usuario en la vista edit_task. En este caso se 
    consideran dos tipos de cambios:
    1. Cambios mayores: estos se refieren a los cambios que cambian la forma en al que se evalua la tarea.
    Estos pueden ser:
        - Eliminar criterios.
        - Modificar puntaje de un criterio.
        - Crear criterios. 
    2. Cambios menores: estos se refieren a los cambios que NO cambian la forma de evaluación:
        - Cambiar nombre de tarea
        - Cambiar datos de un criterios ya existente (se supone que se referira a lo mismo)
    
    Cuando los cambios son mayores, todas las revisiones ya hechas se eliminan.
    """

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
            task.criteria.append(new_criterion)

        else:
            flash("Se ingresaron parametros vacios al intentar creas nuevos criterios")
    
    # En caso de haberse hecho cambios mayores
    if (major_changes):
        # Eliminamos todas las revisiones obsoletas
        for submission in task.submissions:
            database.delete_all(submission.reviews)
    
    database.commit_changes()

    if (major_changes):
        flash("Se modificó la tarea exitosamente y se desecharon las revisiones obsoletas")
    else:
        flash("Se modificó la tarea exitosamente")

    return redirect(url_for("tutor.course", course_id=task.course.id))


@tutor.route("/c/<course_id>/t/<task_id>/submissions", methods=["GET"])
@login_required("TUTOR")
def task_submissions(course_id, task_id):
    """
    En esta vista se muestran todas las revisiones generadas con el ALGORITMO. En cada revision el tutor puede:
    1. Aceptar la revisión generada por el ALGORITMO
    2. Hacer una revisión manual
    """
    # Aquí necesitamos a los estudiantes de un curso, los puntajes obtenidos en la tarea, 
    return render_template("tutor/task_submissions.html",
                           course_id = course_id,
                           task_id= task_id) 


@tutor.route("/c/<course_id>/t/<task_id>/s/<submission_id>", methods=["POST"])
@login_required("TUTOR")
def task_submissions_post(course_id, task_id, submission_id):
    """
    Dado la acción seleccionada por el usuario, se hacen las siguientes acciónes:
    1. Aceptar todas las revisiones
    2. Aceptar una revisión en especifico
    3. Revisar manualmente una revisión
    """
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

@tutor.route("/s/<submission_id>", methods=["GET"])
@login_required("TUTOR")
def submission(submission_id):
    """
    En esta vista se puede revisar una tarea hecha por un estudiante.
    """
    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    submission = database.get_from_id(Submission, submission_id)

    # Revisamos si ya existe una revisión del tutor
    status = "NO REVISADO"
    tutor_review = None
    score = 0
    for review in submission.reviews:
        if review.reviewer == tutor:
            status = "REVISADO"
            tutor_review = review
            for criterion_review in review.criterion_reviews:
                score += criterion_review.score

    return render_template(
        "tutor/submission.html",
        submission=submission,
        estado = status,
        review=tutor_review,
        score = score,
        task_max_score = database.task_max_score(submission.task)
    )


@tutor.route("/s/<submission_id>", methods=["POST"])
@login_required("TUTOR")
def review_submission(submission_id):
    """
    En esta vista se corre la logica de revisar tarea estudiante, los datos se sacan de lo entregado por el
    usuario en submission
    """
    if (False):
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

    # Obtenemos las variables a usar
    tutor = database.set_tutor(session["user_id"])
    submission = database.get_from_id(Submission, submission_id)
    review = Review(submission = submission, reviewer = tutor)
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
            return redirect(url_for("tutor.submission", submission_id))
    
    database.add(review)
    database.add_all(criterion_review_list)
    review.is_pending = False
    database.commit_changes()
    flash("Revision enviada exitosamente")

    return redirect(url_for("tutor.submission", submission_id=submission_id))
