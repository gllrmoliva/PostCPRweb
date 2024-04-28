from . import tutor
from flask import render_template, request, redirect, url_for, session, flash
from login_required import login_required
from database import db
import sqlite3

@tutor.route("/", methods=['GET', 'POST'])
@login_required('tutor')
def hometutor():

    database = db.Connection()
    database.connect()

    user = database.get_user(session['user_id'])

    courses = database.get_courses_from_tutor(user)


    if request.method == 'GET':
        return render_template('tutor/home.html', courses = courses)
    elif request.method == 'POST':
        request_form = request.form
        if request_form['type'] == 'course':
            if request_form['action'] == 'edit':
                return "estás editando el curso"
            elif request_form['action'] == 'enter': 
                # para debugging, esto retorna el dictionary curso:
                # return str(database.get_course(request_form['id']))
                # Miembros de CURSO: {'id','name','tutor_id'} 
                return redirect(url_for('tutor.coursetutor', courseid=int(request_form['id'])))
        if request_form['type'] == 'create_course':
            try:
                database.add_course(request_form['name'], user)

                return redirect(url_for('tutor.hometutor'))
            except sqlite3.IntegrityError:
                flash('Ya existe un curso con ese nombre')
                return redirect(url_for('tutor.hometutor'))


@tutor.route("/c/<int:courseid>", methods=['GET', 'POST'])
@login_required('tutor')
def coursetutor(courseid):

    database = db.Connection()
    database.connect()

    tutor = database.get_user(session['user_id'])
    course = database.get_course(courseid)

    if request.method == 'GET':

        if (course in database.get_courses_from_tutor(tutor)):
            tasks = database.get_tasks_from_course(course)
            return render_template('tutor/course.html', course = course, tasks=tasks)
        else:
            flash('No se puede acceder a ese curso')
            return redirect(url_for('tutor.hometutor'))

    elif request.method == 'POST':
        return "se hizo una peticion post a coursetutor"

@tutor.route("/t/<task_id>", methods=['GET', 'POST'])
@login_required('tutor')
def tasktutor(task_id):
    database = db.Connection()
    database.connect()

    task = database.get_task(task_id)
    criteria = database.get_criteria_of_task(task)

    if request.method == 'GET':
        return render_template("tutor/tasktutor.html", task = task, criteria = criteria)
    elif request.method == 'POST':
        return "metodo post en tasktutor"