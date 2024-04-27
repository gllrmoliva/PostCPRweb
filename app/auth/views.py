from . import auth 
from flask import render_template, request, redirect, url_for, flash, get_flashed_messages

from werkzeug.security import generate_password_hash, check_password_hash

from database import db

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

        email = request_form['email']
        password = request_form['password']

        # si quiero hashear la contraseña
        # password = generate_password_hash(request_form['password'], method="pbkdf2") 

        # Quizas se deba refactorizar despues
        # TODO: ver como se va a cerrar la base de datos
        database = db.Connection()
        database.connect()

        user = database.get_user_from_email(email)

        # verificamos que el usuario exista y la contraseña este correcta        
        if not user or not (user['password'] == password):
            flash('Email o Contraseña equivocado, intente con otro')
            return redirect(url_for('auth.signin'))
        else:
            if ('signinstudent' in request_form) and (database.is_student(user)):
                    return redirect(url_for('student.homestudent'))
            elif ('signintutor' in request_form) and (database.is_tutor(user)):
                    return redirect(url_for('tutor.hometutor'))
            else:
                flash('Email o Contraseña equivocado, intente con otro')
                return redirect(url_for('auth.signin'))