from . import auth 
from flask import render_template, request, redirect, url_for, flash, session

from werkzeug.security import generate_password_hash, check_password_hash

from database import db

"""
Aquí se puede iniciar sesión como estudiante o tutor. Si se apreta el botón iniciar sesión como tutor, se verifica
si el usuario existe, si es así verificamos la contraseña y que sea tutor. Si cumple esto se inicia sesión, si no 
muestra un mensaje tipo no se pudo iniciar sesion. Lo mismo ocurre con estudiante.
"""

@auth.route("/", methods = ['GET'])
def signin():
    """
    En esta ruta se pueden completar los campos correo y contraseña los cuales son manejados en signin_post().
    Solo se muestra si es que en la variable global "session" no existen los campos 'user_id' y 'user_type', si no
    es así, te envía a la pagina home de cada tipo de usuario.
    """

    if request.method == 'GET':
        if 'user_type' in session and 'user_id' in session:
            if session['user_type'] == 'tutor':
                return redirect(url_for('tutor.hometutor'))
            elif session['user_type'] == 'student':
                return redirect(url_for('student.homestudent'))

        return render_template("signin.html")

@auth.route("/", methods = ['POST'])
def signin_post():
    """
    Aquí recuperamos los datos entregados por el usuario, luego verificamos si el usuario existe 
    y si la contraseña recuperada corresponde con la guardada en la base de datos. Si es así, 
    verificamos que el usuario corresponda con tipo de inicio de sesión presionado. Si esto se cumple,
    lo redirigimos a la home del tipo de usuario seleccionado. 
    """

    # Recuperamos los datos del formulario de inicio de sesión enviados
    request_form = request.form

    email = request_form['email']
    password = request_form['password']

    # Iniciamos la base de datos, además aqui se estan creando las tablas y añadiendo datos de prueba
    # FIXME: esto se tendra que cambiar con el uso de SQLAlchemy
    database = db.Connection()
    database.connect()
    database.create_tables()
    database.fill_tables_with_examples()

    # obtenemos al usuario de la base de datos a partir del email, y lo guardamos
    user = database.get_user_from_email(email)

    # Si el usuario no existe o la contraseña no es la misma que en la base de datos
    # renderizamos signin.html, pero esta vez mostrando un mensaje, esto lo hacemos a traves del comando
    # flash, el cual luego es manejado en el html con jinja
    if not user or not (user['password'] == password):
        flash('Email o Contraseña equivocado, intente con otro')
        return redirect(url_for('auth.signin'))
    else:
        # Si el usuario existe y la contraseña esta correcta, vemos cual de los botones se apretaron
        # si se apreto el boton de iniciar sesión como estudiante, verificamos que efectivamente el usuario es un
        # estudiante y guardamos el id y el tipo de usuario en una variable global de flask llamada session, esta variable se 
        # puede utilizar en cualquier ruta de la web, para el boton iniciar sesion como tutor se hace lo mismo
        if 'signinstudent' in request_form and database.is_student(user):
            session['user_id'] = user['id']
            session['user_type'] = 'student'
            return redirect(url_for('student.homestudent'))
        elif 'signintutor' in request_form and database.is_tutor(user):
            session['user_id'] = user['id']
            session['user_type'] = 'tutor'
            return redirect(url_for('tutor.hometutor'))
        
        # Si es que por alguna razon el usuario no es tutor ni estudiante, entonces lo atajamos aquí, 
        # igualmente creo que esta función es media inutil, ya que nunca se deberia llegar hasta aquí
        else:
            flash('Email o Contraseña equivocado, intente con otro (tipo de usuario no definido)')
            return redirect(url_for('auth.signin'))



# Ruta a la que se accede cuando se quiere cerrar sesión
@auth.route("/logout")
def logout():
    """
    Ruta a la que se accede al querer cerrar sesion, en esta se borran los datos de la variable global session
    y luego se manda hacia la ruta singin, donde se logea el usuario
    """
    
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.signin'))