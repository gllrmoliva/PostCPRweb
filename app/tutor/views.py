from . import tutor
from flask import render_template, request, redirect, url_for, session, flash
from login_required import login_required
from database import db
import sqlite3
from database.models import engine
from sqlalchemy.orm import sessionmaker
from database.models import *
from database.schemas import Database

database = Database(engine)


@tutor.route("/", methods=["GET", "POST"])
@login_required("tutor")
def hometutor():

    user = database.get_user(session["user_id"])

    courses = database.get_courses_from_tutor(user)

    if request.method == "GET":
        return render_template("tutor/home.html", courses=courses)
    elif request.method == "POST":
        request_form = request.form
        print("REQUEST_FORM", request_form)
        if request_form["type"] == "course":
            if request_form["action"] == "edit":
                return redirect(
                    url_for("tutor.editcourse", courseid=int(request_form["id"]))
                )
                return "estás editando el curso"
            elif request_form["action"] == "enter":
                return redirect(
                    url_for("tutor.coursetutor", courseid=int(request_form["id"]))
                )
        if request_form["type"] == "create_course":
            try:
                database.add_course(request_form["name"], user)

                return redirect(url_for("tutor.hometutor"))
            except Exception as e:
                flash(f"Exception {e}")
                return redirect(url_for("tutor.hometutor"))


@tutor.route("/c/<int:courseid>", methods=["GET", "POST"])
@login_required("tutor")
def coursetutor(courseid):

    tutor = database.get_user(session["user_id"])
    course = database.get_course(courseid)

    if request.method == "GET":

        tasks = database.get_tasks_from_course(course)
        return render_template("tutor/course.html", course=course, tasks=tasks)

    elif request.method == "POST":
        request_form = request.form
        # si se presiona el botón crear tarea y se crea una tarea
        if request_form["type"] == "create_task":
            name = request_form["name"]
            instructions = request_form["instructions"]

            try:
                database.add_task(name, instructions, course)
            except Exception as Error:
                # TODO: poner un nombre de error mas demostrativo
                flash(Error)

            tasks = database.get_tasks_from_course(course)
            return render_template("tutor/course.html", course=course, tasks=tasks)

        return "se hizo una peticion post a coursetutor"


@tutor.route("/c/<int:courseid>/edit", methods=["GET", "POST"])
@login_required("tutor")
def editcourse(courseid):

    tutor = database.get_user(session["user_id"])
    course = database.get_course(courseid)

    if request.method == "GET":
        return render_template("tutor/editcourse.html")

    elif request.method == "POST":
        return "se hizo una peticion post a editcurso"


@tutor.route("/t/<task_id>", methods=["GET", "POST"])
@login_required("tutor")
def tasktutor(task_id):

    task = database.get_task(task_id)
    criteria = database.get_criteria_from_task(task)
    print(f"TASK: {task}")
    if request.method == "GET":
        return render_template("tutor/tasktutor.html", task=task, criteria=criteria)
    elif request.method == "POST":
        return "metodo post en tasktutor"
