from flask import Flask, redirect, render_template,request, url_for

app = Flask(__name__)

# Pagina de inicio de sesión
@app.route("/", methods = ['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")
    elif request.method == 'POST':
        request_form = request.form
        if 'signinstudent' in request_form:
            return redirect(url_for('homestudent')) 
        elif 'signintutor' in request_form:
            return redirect(url_for('hometutor')) 
    
# pagina de cursos profesor, quizas cambiar el nombre a /tutor/cursos
@app.route("/tutor", methods = ['GET', 'POST'])
def hometutor():
    if request.method == 'GET':
        # Claramente el Cursos, debe ser sacado con una función de backend la cual de de output los cursos, con sus caracteristicas
        return render_template('tutor/home.html',cursos = ['Lenguaje', 'Matematicas', 'Historia'])

#pagina de cursos alumno, quizas cambiar el nombre a /student/cursos
@app.route("/student", methods = ['GET', 'POST'])
def homestudent():
    if request.method == 'GET':
        return render_template('student/home.html',cursos = ['Lenguaje', 'Matematicas', 'Historia'])