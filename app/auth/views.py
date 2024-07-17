from . import auth
from flask import render_template, request, redirect, url_for, flash, session

from database.database import Database
from database.database import User

"""
Aquí se puede iniciar sesión como estudiante o tutor. Si se apreta el botón iniciar sesión como tutor, se verifica
si el usuario existe, si es así verificamos la contraseña y que sea tutor. Si cumple esto se inicia sesión, si no 
muestra un mensaje tipo no se pudo iniciar sesion. Lo mismo ocurre con estudiante.
"""

# Los valores por defecto de la BDD originalmente eran insertados desde un archivo .py ejecutado desde el root del proyecto, sólo los dejé acá porque vi que esta era la primera incialización de ``Database`` - Martín

database = Database()
database.init()

@auth.route("/", methods = ['GET'])
def signin():
    """
    En esta ruta se pueden completar los campos correo y contraseña los cuales son manejados en signin_post().
    Solo se muestra si es que en la variable global "session" no existen los campos 'user_id' y 'user_type', si no
    es así, te envía a la pagina home de cada tipo de usuario.
    """

    # Si accedemos con el metodo get, verificamos si hay datos guardados en session, si los hay
    # te redirige inmediatamente a la pagina de tutor o student segun corresponda
    # si no hay datos guardados puedes iniciar sesion
    if "user_type" in session and "user_id" in session:
        if session["user_type"] == "TUTOR":
            return redirect(url_for("tutor.home"))
        elif session["user_type"] == "STUDENT":
            return redirect(url_for("student.home"))
        elif session["user_type"] == 'ADMIN':
            return redirect(url_for("admin.home"))

    return render_template("signin.html")

@auth.route("/", methods = ['POST'])
def signin_post():
    """
    En esta ruta se reciben los datos con los cuales quiere acceder el usuario. 
    Se inicia sesión si son correctos.
    """
        
    # Recuperamos los datos del formulario de inicio de sesión enviados
    request_form = request.form

    email = request_form["email"]
    password = request_form["password"]
    print(f"{email} {password}")
    # Iniciamos la base de datos, además aqui se estan creando las tablas y añadiendo datos de prueba
        # yo aqui no veo nada xd???


    # Diferenciamos si el usuario inicia sesión como estudiante o como tutor    TODO: y como admin
    # Login como estudiante
    if email == "admin@admin.com" and password == "admin":
            session["user_id"] = -1 
            session["user_type"] = "ADMIN"
            return redirect(url_for("admin.home"))
    elif "signinstudent" in request_form:
        student = database.login_student(email, password)
        # Login incorrecto
        if (student == None):
            flash("Email o Contraseña equivocado, intente con otro")
            return redirect(url_for("auth.signin"))
        # Login correcto
        else:
            session["user_id"] = student.id
            session["user_type"] = "STUDENT"
            return redirect(url_for("student.home"))
    # Login como tutor
    elif "signintutor" in request_form:
        tutor = database.login_tutor(email, password)
        # Login incorrecto
        if (tutor == None):
            flash("Email o Contraseña equivocado, intente con otro")
            return redirect(url_for("auth.signin"))
        # Login correcto
        else:
            session["user_id"] = tutor.id
            session["user_type"] = "TUTOR"
            return redirect(url_for("tutor.home"))
    # no sé en que caso se llegaria a aca, pero por si acaso
    else:
        flash("Inicio de sesión invalido")
        return redirect(url_for("auth.signin"))

        # deprecated
        if (False):
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
                    return redirect(url_for("student.home"))
                elif "signintutor" in request_form and database.is_tutor(user):
                    session["user_id"] = user.id
                    session["user_type"] = "tutor"
                    return redirect(url_for("tutor.home"))

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
    """
    Ruta a la que se accede al querer cerrar sesion, en esta se borran los datos de la variable global session
    y luego se manda hacia la ruta singin, donde se logea el usuario
    """
    
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.signin"))


# Ruta a la que se accede cuando se quiere cerrar sesión
@auth.route("/account", methods = ['GET'])
def account():
    """
    En esta ruta se introducen los cambios que un usuario quiere hacer en su cuenta. Estos son:
    1. Cambio de Username
    2. Cambio de Correo
    3. Cambio de Contraseña
    """
    
    if "user_type" in session and "user_id" in session:
        user = database.get_from_id(User, session["user_id"])
        return render_template("account.html", user=user)
    else:
        flash("Para acceder a esta página debes iniciar sesión")

    return redirect(url_for("auth.signin"))

@auth.route("/account", methods = ['POST'])
def account_post():
    """
    La función recibe un formulario con las peticiones de cambios del usuario. Los cambios que se pueden realizar
    son:
    1. Cambiar el nombre del usuario
    2. Cambiar el correo del usuario
    3. Cambiar la contraseña
    Para hacer cualquiera de estar acciones se debe confirmar con la contraseña actual del usuario.
    Nota: Si no se completa el campo "nueva contraseña" la contraseña no se cambia.
    """

    # Obtenemos al usuario
    if "user_type" in session and "user_id" in session:
        user = database.get_from_id(User, session["user_id"])
    else:
        flash("Para acceder a esta página debes iniciar sesión")
        return redirect(url_for("auth.signin"))
    
    form = request.form

    # La contraseña nueva no se ingresó dos veces
    if form["newPassword"] != form["confirmPassword"]:
        flash("La confirmación de la contraseña nueva no coincide. Ingresé la contraseña nueva dos veces")
        return redirect(url_for("auth.account"))
    
    # La contraseña antigua es incorrecta
    if form["currentPassword"] != user.password:
        flash("La contraseña actual ingresada es incorrecta")
        return redirect(url_for("auth.account"))
    
    name_changed = False
    email_changed = False
    password_changed  = False

    if form["username"] != user.name:
        user.name = form["username"]
        name_changed = True
    if form["email"] != user.email:
        user.email = form["email"]
        email_changed = True
    if form["newPassword"] != user.password and form["newPassword"] != "":
        user.password = form["newPassword"]
        password_changed = True

    database.commit_changes()

    flash_message = ""
    if name_changed: flash_message += "Nombre cambiado exitosamente. "
    if email_changed: flash_message += "Correo electrónico cambiado exitosamente."
    if password_changed: flash_message += "Contraseña cambiada exitosamente. "

    if flash_message != "":
        flash(flash_message)

    return redirect(url_for("auth.account"))