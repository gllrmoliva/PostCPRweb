from . import auth 
from flask import render_template, request, redirect, url_for
import fakedatabase

"""
Aquí se puede iniciar sesión como estudiante o tutor. Si se apreta el botón iniciar sesión como tutor, se verifica
si el usuario existe, si es así verificamos la contraseña y que sea tutor. Si cumple esto se inicia sesión, si no 
muestra un mensaje tipo no se pudo iniciar sesion. Lo mismo ocurre con estudiante.
"""
@auth.route("/", methods = ['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")

    elif request.method == 'POST':
        request_form = request.form
        # Esto es solo para el primer sprint
        if 'signinstudent' in request_form:
            if (fakedatabase.studentInDB(request_form['email'], request_form['password'])):
                return redirect(url_for('student.homestudent'))
            else:
                return render_template("signin.html", error_message = 'Email o Contraseña equivocado, intente con otro')

        elif 'signintutor' in request_form:
            if (fakedatabase.tutorInDB(request_form['email'], request_form['password'])):
                return redirect(url_for('tutor.hometutor'))
            else:
                return render_template("signin.html", error_message = 'Email o Contraseña equivocado, intente con otro')
