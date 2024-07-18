from . import admin
from flask import render_template, request, redirect, url_for, session, flash

from login_required import login_required
from database.database import Database
from database.database import User, Student, Tutor

"""
Todas las rutas que están aquí tienen el prefijo "/admin"
"""

# En caso de que se desee restablacer contraseña, esta contraseña será la provisional
default_password = "1234"

database = Database()
database.init()

@admin.route("/", methods=["GET"])
@login_required('ADMIN')
def home():

    # Obtenemos las variables a usar
    users = database.get_all(User)

    return render_template("admin/home.html", users=users)

@admin.route("/", methods=["POST"])
@login_required('ADMIN') 
def home_post():
    form = request.form

    # En caso de que se quiera crear un nuevo usuario
    if (form['form_type'] == "create_new_user"):

        email = form["email"]
        # Verificamos que el correo no se repita
        if database.get_from(User, User.email, email) != None:
            flash("Ya existe un usuario con el correo ingresado")
            return redirect(url_for("admin.home"))
        
        if form["user_type"] == "STUDENT":
            new_user = Student(name = form["name"], email = email)
        elif form["user_type"] == "TUTOR":
            new_user = Tutor(name = form["name"], email = email)

        # Contraseña por defecto
        new_user.password = default_password

        database.add(new_user)
        database.commit_changes()
        flash("Usuario añadido existosamente")

    elif (form['form_type'] == "clear_database"):
        database.clear()
        flash("Se ha limpiado la base de datos exitosamente")

    elif (form['form_type'] == "add_example_values"):

        flash("Se cargo la base de datos de ejemplo")

    # En caso de que se quiera modificar / eliminar un usuario
    elif (form['form_type'] == "edit_user"):

        # Obtenemos al usuario
        user = database.get_from_id(User, form["user_id"])

        if 'modify' in form:

            # Restablecer contraseña
            if 'reset_password' in form:
                user.password = default_password

            database.commit_changes()
            flash("Se ha restablecido la contraseña del usuario exitosamente")

        elif 'delete' in form:

            # CONFIAMOS EN LA CASCADA
            database.delete(user)
            database.commit_changes()
            flash("Se ha removido la cuenta del usuario exitosamente")

    return redirect(url_for("admin.home"))