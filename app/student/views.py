from . import student 
from flask import render_template, request, redirect, url_for
import database

# RUTAS STUDIANTE
#pagina de cursos alumno, quizas cambiar el nombre a /student/cursos
@student.route("/student", methods = ['GET', 'POST'])
def homestudent():
    request_form = request.form
    if request.method == 'GET':
        # Claramente el Cursos, debe ser sacado con una función de backend la cual de de output los cursos, con sus caracteristicas
        return render_template('student/home.html',cursos = database.get_cursos())
    if request.method == 'POST':
        request_form = request.form
        if request_form['type'] == 'course':
            if request_form['action'] == 'enter':
                #TODO: agregar vista de que se vera en el curso
                return "estas entrando a un curso"


# TODO:hay que implementar esto aaaaaaaaaaaaaa
@student.route("/student/c/<int:courseid>", methods = ['GET', 'POST'])
def coursestudent(courseid):
    if request.method == 'GET':
        return render_template('student/course.html', courseid = courseid)
    elif request.method == 'POST':
        request_form = request.form
        if request_form['type'] == 'course':
            if request_form['action'] == 'enter':
                #TODO: agregar vista de que se vera en el curso
                return "estas entrando a un curso"


@student.route("/student/h", methods = ['GET', 'POST'])
def homeworksstudent():
    if request.method == 'GET':
        return render_template('student/homeworks.html')
    elif request.method == 'POST':
        return render_template('algo')