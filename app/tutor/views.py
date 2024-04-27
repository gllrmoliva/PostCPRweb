from . import tutor
from flask import render_template, request, redirect, url_for
from login_required import login_required
import fakedatabase

@tutor.route("/", methods=['GET', 'POST'])
@login_required('tutor')
def hometutor():
    if request.method == 'GET':
        return render_template('tutor/home.html', cursos=fakedatabase.get_cursos())
    elif request.method == 'POST':
        request_form = request.form
        if request_form['type'] == 'course':
            if request_form['action'] == 'edit':
                return "estás editando el curso"
            elif request_form['action'] == 'enter': 
                return redirect(url_for('tutor.coursetutor', courseid=request_form['id']))
        if request_form['type'] == 'create_course':
            fakedatabase.crear_curso(request_form['name'], request_form['description'])
            return redirect(url_for('tutor.hometutor'))

@tutor.route("/c/<courseid>", methods=['GET', 'POST'])
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