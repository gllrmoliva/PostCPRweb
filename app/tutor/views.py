from . import tutor
from flask import render_template, request, redirect, url_for, session, flash
from login_required import login_required
from database import db
import sqlite3

@tutor.route("/", methods=['GET'])
@login_required('tutor')
def hometutor():

    # Aqui accedemos a la base de datos
    database = db.Connection()
    database.connect()

    # Recuperamos de la base de datos el usuario, para luego recuperar los cursos
    user = database.get_user(session['user_id'])
    courses = database.get_courses_from_tutor(user)

    # A render_template le damos la variable courses, ya que jinja lo usa para mostrar los cursos del
    # usuario (ver tutor/home.html para ver como es utilizado courses)
    return render_template('tutor/home.html', courses = courses)


@tutor.route("/", methods=['POST'])
@login_required('tutor')
def hometutor_post():

    # Accedemos a la base de datos
    database = db.Connection()
    database.connect()

    # Recuperamos de la base de datos el usuario, para luego recuperar los cursos
    user = database.get_user(session['user_id'])

    # Obtenemos los datos del formulario
    request_form = request.form

    # Notemos que en tutor/home.html, los forms tienen 2 propiedades importantes name y value
    # para obtener los datos podemos hacer lo siguiente request.form['name'] = value
    # entonces: 
    # - si form_type es create_course, intentamos crear el curso con el nombre dado. Si esto no funciona
    #   enviamos al usuario a home
    if request_form['form_type'] == 'create_course':
        try:
            database.add_course(request_form['name'], user)

            return redirect(url_for('tutor.hometutor'))
        except sqlite3.IntegrityError:
            flash('Ya existe un curso con ese nombre')
            return redirect(url_for('tutor.hometutor'))
        except Exception as e:
            flash(e)
            return redirect(url_for('tutor.hometutor'))


@tutor.route("/c/<int:courseid>", methods=['GET'])
@login_required('tutor')
def coursetutor(courseid):

    # Accedemos a la base de datos
    database = db.Connection()
    database.connect()

    # Obtenemos al usuario(tutor) y el curso (con el id)
    tutor = database.get_user(session['user_id'])
    course = database.get_course(courseid)

    # Si el tutor pertenece al curso:
    # - se obtienen las tareas del curso y se renderiza la template tutor/course.html
    # Si el tutor no pertenece al curso:
    # - Se envia al usuario a home y se muestra una advertencia en pantalla (flash)
    if (course in database.get_courses_from_tutor(tutor)):
        tasks = database.get_tasks_from_course(course)
        return render_template('tutor/course.html', course = course, tasks=tasks)
    else:
        flash('No se puede acceder a ese curso')
        return redirect(url_for('tutor.hometutor'))


@tutor.route("/c/<int:courseid>", methods=['POST'])
@login_required('tutor')
def coursetutor_post(courseid):

    # Accedemos a la base de datos
    database = db.Connection()
    database.connect()

    # Obtenemos el curso (con el id)
    course = database.get_course(courseid)

    # Obtenemos los datos presionados por el usuario
    request_form = request.form

    # Si se presiona el botón crear tarea:
    # - Se recuperan los datos del formulario.
    # - intentamos crear el curso, si no se puede, se muestra el error en pantalla
    if request_form['form_type'] == 'create_task':

        name = request_form['name']
        instructions = request_form['instructions']

        try: 
            database.add_task(name,instructions,course)
        except Exception as Error:
            # TODO: cambiar el error por algo mas descriptivo 
            flash(str(Error))

        return redirect(url_for('tutor.coursetutor', courseid = courseid))

    return "se hizo una peticion post a coursetutor: " + str(request_form)


@tutor.route("/c/<int:courseid>/edit", methods=['GET'])
@login_required('tutor')
def editcourse(courseid):

    # Accedemos a la base de datos
    database = db.Connection()
    database.connect()

    # recuperamos al usuario(tutor) y el curso que queremos editar
    tutor = database.get_user(session['user_id'])
    course = database.get_course(courseid)

    # si el curso pertenece al tutor, entonces se muestra el editar curso
    # si no es así, se redirige al usuario hacia el home y se muestra una advertencia en pantalla (flash)
    if (course in database.get_courses_from_tutor(tutor)):
        return render_template('tutor/editcourse.html')
    else:
        flash('No se puede acceder a ese curso')
        return redirect(url_for('tutor.hometutor'))


@tutor.route("/c/<int:courseid>/edit", methods=['POST'])
@login_required('tutor')
def editcourse_post(courseid):
    request_form = request.form()
    return "se hizo una peticion post a editcurso: " + str(request_form)


@tutor.route("/t/<task_id>", methods=['GET'])
@login_required('tutor')
def tasktutor(task_id):

    # accedemos a la base de datos
    database = db.Connection()
    database.connect()

    # Obtenemos la tarea y los criterios de la tarea
    task = database.get_task(task_id)
    criteria = database.get_criteria_of_task(task)

    return render_template("tutor/tasktutor.html", task = task, criteria = criteria)

@tutor.route("/t/<task_id>", methods=['POST'])
@login_required('tutor')
#TODO hacer esta ruta
def tasktutor_post(task_id):
    return "metodo post en tasktutor"