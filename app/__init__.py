from flask import Flask

def create_app():
    app = Flask(__name__)

    from .tutor import tutor as tutor_blueprint
    app.register_blueprint(tutor_blueprint, url_prefix='/tutor')

    from .student import student as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/student')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
