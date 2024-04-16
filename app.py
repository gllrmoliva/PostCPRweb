from flask import Flask, redirect, render_template,request, url_for
import database
app = Flask(__name__)

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
    
# pagina de cursos profesor, quizas cambiar el nombre a /tutor/cursos
@app.route("/tutor", methods = ['GET', 'POST'])
def hometutor():
    if request.method == 'GET':
        # Claramente el Cursos, debe ser sacado con una función de backend la cual de de output los cursos, con sus caracteristicas
        return render_template('tutor/home.html',cursos = ['Lenguaje', 'Matemáticas', 'Historia'])

#pagina de cursos alumno, quizas cambiar el nombre a /student/cursos
@app.route("/student", methods = ['GET', 'POST'])
def homestudent():
    if request.method == 'GET':
        return render_template('student/home.html',cursos = ['Lenguaje', 'Matemáticas'])