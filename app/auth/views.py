from . import auth 
from flask import render_template, request, redirect, url_for
import database


@auth.route("/", methods = ['GET', 'POST'])
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
