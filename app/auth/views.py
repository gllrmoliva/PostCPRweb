from . import auth
from flask import render_template, request, redirect, url_for, flash, session

from werkzeug.security import generate_password_hash, check_password_hash

from database.models import engine
from database.schemas import Database

"""
Aquí se puede iniciar sesión como estudiante o tutor. Si se apreta el botón iniciar sesión como tutor, se verifica
si el usuario existe, si es así verificamos la contraseña y que sea tutor. Si cumple esto se inicia sesión, si no 
muestra un mensaje tipo no se pudo iniciar sesion. Lo mismo ocurre con estudiante.
"""

database = Database(engine)


@auth.route("/", methods=["GET", "POST"])
def signin():

    # Si accedemos con el metodo get, verificamos si hay datos guardados en session, si los hay
    # te redirige inmediatamente a la pagina de tutor o student segun corresponda
    # si no hay datos guardados puedes iniciar sesion
    if request.method == "GET":
        if "user_type" in session and "user_id" in session:
            if session["user_type"] == "tutor":
                return redirect(url_for("tutor.hometutor"))
            elif session["user_type"] == "student":
                return redirect(url_for("student.homestudent"))

        return render_template("signin.html")

    # Al accederse con el metodo post
    elif request.method == "POST":
        # Recuperamos los datos del formulario de inicio de sesión enviados
        request_form = request.form

        email = request_form["email"]
        password = request_form["password"]
        print(f"{email} {password}")
        # Iniciamos la base de datos, además aqui se estan creando las tablas y añadiendo datos de prueba

        # tengo miedo sobre que pasa si no se cierra la sesión

        # obtenemos al usuario de la base de datos a partir del email, y lo guardamos
        user = database.get_user_from_email(email)
        # Si el usuario no existe o la contraseña no es la misma que en la base de datos
        # renderizamos signin.html, pero esta vez mostrando un mensaje, esto lo hacemos a traves del comando
        # flash, el cual luego es manejado en el html con jinja
        if not user or not (user.password == password):
            flash("Email o Contraseña equivocado, intente con otro")
            return redirect(url_for("auth.signin"))
        else:
            # Si el usuario existe y la contraseña esta correcta, vemos cual de los botones se apretaron
            # si se apreto el boton de iniciar sesión como estudiante, verificamos que efectivamente el usuario es un
            # estudiante y guardamos el id y el tipo de usuario en una variable global de flask llamada session, esta variable se
            # puede utilizar en cualquier ruta de la web, para el boton iniciar sesion como tutor se hace lo mismo
            if "signinstudent" in request_form and database.is_student(user):
                session["user_id"] = user.id
                session["user_type"] = "student"
                return redirect(url_for("student.homestudent"))
            elif "signintutor" in request_form and database.is_tutor(user):
                session["user_id"] = user.id
                session["user_type"] = "tutor"
                return redirect(url_for("tutor.hometutor"))

            # Si es que por alguna razon el usuario no es tutor ni estudiante, entonces lo atajamos aquí,
            # igualmente creo que esta función es media inutil, ya que nunca se deberia llegar hasta aquí
            else:
                flash(
                    "Email o Contraseña equivocado, intente con otro (tipo de usuario no definido)"
                )
                return redirect(url_for("auth.signin"))


# Ruta a la que se accede cuando se quiere cerrar sesión
@auth.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.signin"))
