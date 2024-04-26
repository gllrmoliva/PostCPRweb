from . import tutor
from flask import render_template, request, redirect, url_for
import database

@tutor.route("/", methods=['GET', 'POST'])
def hometutor():
    if request.method == 'GET':
        return render_template('tutor/home.html', cursos=database.get_cursos())
    elif request.method == 'POST':
        request_form = request.form
        if request_form['type'] == 'course':
            if request_form['action'] == 'edit':
                return "estás editando el curso"
            elif request_form['action'] == 'enter': 
                return redirect(url_for('tutor.coursetutor', courseid=request_form['id']))
        if request_form['type'] == 'create_course':
            database.crear_curso(request_form['name'], request_form['description'])
            return redirect(url_for('tutor.hometutor'))

@tutor.route("/c/<courseid>", methods=['GET', 'POST'])
def coursetutor(courseid):
    curso = database.get_curso(courseid)
    return render_template('tutor/course.html', curso=curso)
