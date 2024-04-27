from . import tutor
from flask import render_template, request, redirect, url_for, session, flash
from login_required import login_required
from database import db
import sqlite3

import fakedatabase

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
                return str(database.get_course(request_form['id']))
                return redirect(url_for('tutor.coursetutor', courseid=request_form['id']))
        if request_form['type'] == 'create_course':
            try:
                # TODO: al crear bases de datos, por alguna razon, cuando ya existe un curso con
                #el nombre que quiero crear en la segunda vez de usar la DB, se freezea sqlite
                database.add_course(request_form['name'], user)

                return redirect(url_for('tutor.hometutor'))
            except sqlite3.IntegrityError:
                flash('Ya existe un curso con ese nombre')
                return redirect(url_for('tutor.hometutor'))


@tutor.route("/c/<int:courseid>", methods=['GET', 'POST'])
@login_required('tutor')
def coursetutor(courseid):
    if request.method == 'GET':
        curso = fakedatabase.get_curso(courseid)
        return render_template('tutor/course.html', curso=curso)
    elif request.method == 'POST':
        return "se hizo una peticion post"

@tutor.route("/t/<taskid>", methods=['GET', 'POST'])
@login_required('tutor')
def tasktutor(taskid):
    return render_template("tutor/tasktutor.html")