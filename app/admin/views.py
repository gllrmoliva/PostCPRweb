from . import admin
from flask import render_template, request, redirect, url_for, session, flash
from login_required import login_required

"""
Todas las rutas que están aquí tienen el prefijo "/admin"
"""

@admin.route("/")
# @login_required('admin') esto se pone cuando ya esté mas o menos lista la base de datos
def logout():
    return "esto es una ruta para el administrador"
