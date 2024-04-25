from flask import Flask, redirect, render_template,request, url_for

import database

app = Flask(__name__)


"""
OJO, creo que estoy haciendo una mala practica, pero realmente no se si es tan así.
basicamente todos los botones los estoy metiendo dentro de un form, esto es malo supongo porque todos los inputs del
usuario estan siendo vistos como forms pero es la solución que encontre al problema sin tener que aprender Js.
se puede manejar todo desde python con if's lo unico malo es que hace un poco menos legible el codigo de html

TODO:
-[] Separar las funciones en archivos, estaba pensando en tutor, student y auth (login register)
-[] Añadir el sistema de hacer acciones tutor/student solo cuando este este logueado 
-[] Hacer documentación del codigo.
"""

# Pagina de inicio de sesión
@app.route("/", methods = ['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")
    elif request.method == 'POST':
        request_form = request.form
        # Esto es solo para el primer sprint
        if 'signinstudent' in request_form:
            if (database.studentInDB(request_form['email'], request_form['password'])):
                return redirect(url_for('homestudent'))
            else:
                return render_template("signin.html", error_message = 'Email o Contraseña equivocado, intente con otro')

        elif 'signintutor' in request_form:
            if (database.tutorInDB(request_form['email'], request_form['password'])):
                return redirect(url_for('hometutor'))
            else:
                return render_template("signin.html", error_message = 'Email o Contraseña equivocado, intente con otro')

# RUTAS TUTOR
    
# pagina de cursos profesor, quizas cambiar el nombre a /tutor/cursos
@app.route("/tutor", methods = ['GET', 'POST'])
def hometutor():
    if request.method == 'GET':

        # Claramente el Cursos, debe ser sacado con una función de backend la cual de de output los cursos, con sus caracteristicas
        return render_template('tutor/home.html',cursos = database.get_cursos())

    elif request.method == 'POST':

        request_form = request.form

        if request_form['type'] == 'course':
            if request_form['action'] == 'edit':
                #TODO: agregar vista de editar curso
                return "estas editando el curso"
            elif request_form['action'] == 'enter':
                return redirect(url_for(coursetutor()) + request_form['id']) 

        if request_form['type'] == 'create_course':
            database.crear_curso(request_form['name'], request_form['description'])

            return redirect(url_for('hometutor'))


# TODO:hay que implementar esto aaaaaaaaaaaaaa
@app.route("/tutor/c/<courseid>", methods = ['GET', 'POST'])
def coursetutor(courseid):

    if request.method == 'GET':
        curso = database.get_curso(courseid)
        return render_template('tutor/course.html', curso = curso)

    elif request.method == 'POST':
        curso = database.get_curso(courseid)
        return render_template('tutor/course.html', curso = curso)

# RUTAS STUDIANTE
#pagina de cursos alumno, quizas cambiar el nombre a /student/cursos
@app.route("/student", methods = ['GET', 'POST'])
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
@app.route("/student/c/<int:courseid>", methods = ['GET', 'POST'])
def coursestudent(courseid):
    if request.method == 'GET':
        return render_template('student/course.html', courseid = courseid)
    elif request.method == 'POST':
        request_form = request.form
        if request_form['type'] == 'course':
            if request_form['action'] == 'enter':
                #TODO: agregar vista de que se vera en el curso
                return "estas entrando a un curso"

@app.route("/student/h", methods = ['GET', 'POST'])
def homeworksstudent():
    if request.method == 'GET':
        return render_template('student/homeworks.html')
    elif request.method == 'POST':
        return render_template('algo')