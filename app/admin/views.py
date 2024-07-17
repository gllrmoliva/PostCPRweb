from . import admin
from flask import render_template, request, redirect, url_for, session, flash

from login_required import login_required
from database.database import Database
from database.database import User

"""
Todas las rutas que están aquí tienen el prefijo "/admin"
"""

# En caso de que se desee restablacer contraseña, esta contraseña será la provisional
defaul_password = "1234"

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
        new_user = User(name = form["name"], email = form["email"])

        # TODO: ¡No hay forma de seleccionar tipo de usuario en la creación!
        new_user.type = "STUDENT" # Estudiante por defecto

        # Contraseña por defecto
        new_user.password = defaul_password

        database.add(new_user)
        database.commit_changes()
        flash("Usuario añadido existosamente")

    # En caso de que se quiera modificar / eliminar un usuario
    elif (form['form_type'] == "edit_user"):

        # Obtenemos al usuario
        user = database.get_from_id(User, form["user_id"])

        if 'modify' in form:

            # Restablecer contraseña
            if 'reset_password' in form:
                user.password = defaul_password

            # Cambiar tipo de usuario
            user.type = form["user_type"]

            database.commit_changes()
            flash("Usuario modificado existosamente.")

        elif 'delete' in form:

            flash(f"ELIMINA: {str(form)}")
            # Aquí solo se deberia hacer al logica de eliminar usuario

    return redirect(url_for("admin.home"))