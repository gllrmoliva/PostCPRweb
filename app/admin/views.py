from . import admin
from flask import render_template, request, redirect, url_for, session, flash

from login_required import login_required
from database import db
from database.models import engine
from sqlalchemy.orm import sessionmaker
from database.models import *
from database.functions import Database
from datetime import date

"""
Todas las rutas que están aquí tienen el prefijo "/admin"
"""

database = Database(engine)

@admin.route("/", methods=["GET"])
@login_required('admin')
def home():
    return render_template("admin/home.html")

@admin.route("/", methods=["POST"])
@login_required('admin') 
def home_post():
    form = request.form
    # En caso de que se quiera crear un nuevo usuario
    if (form['form_type'] == "create_new_user"):
        flash(f"Se creo el usuario:{str(form)}")
    # En caso de que se quiera modificar / eliminar un usuario
    elif (form['form_type'] == "edit_user"):
        if 'modify' in form:
            if 'reset_password' in form:
                pass
            # TODO: Poner función para cambiar el tipo de usuario.
            flash(f"MODIFICA: {str(form)}")
        elif 'delete' in form:
            flash(f"ELIMINA: {str(form)}")
            # Aquí solo se deberia hacer al logica de eliminar usuario

    return redirect(url_for("admin.home"))