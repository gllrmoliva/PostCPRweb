from . import auth 
from flask import render_template, request, redirect, url_for, flash, session

from werkzeug.security import generate_password_hash, check_password_hash

from database import db

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

        email = request_form['email']
        password = request_form['password']

        database = db.Connection()
        database.connect()
        # tengo miedo sobre que pasa si no se cierra la sesión

        user = database.get_user_from_email(email)

        if not user or not (user['password'] == password):
            flash('Email o Contraseña equivocado, intente con otro')
            return redirect(url_for('auth.signin'))
        else:
            session['user_id'] = user['id']
            
            if 'signinstudent' in request_form and database.is_student(user):
                session['user_id'] = 'student'
                return redirect(url_for('student.homestudent'))
            elif 'signintutor' in request_form and user['type'] == 'tutor':
                session['user_id'] = 'tutor'
                return redirect(url_for('tutor.hometutor'))
            else:
                flash('Email o Contraseña equivocado, intente con otro')
                return redirect(url_for('auth.signin'))

@auth.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.signin'))