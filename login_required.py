# hay que cambiar esto de ruta
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(user_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debe iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.signin'))
            elif session['user_type'] != user_type:
                flash('No tiene permiso para acceder a esta página.', 'warning')
                return redirect(url_for('auth.signin'))
            return func(*args, **kwargs)
        return wrapper
    return decorator
