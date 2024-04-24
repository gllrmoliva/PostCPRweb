import random

student = { 'email':'student@student.com',
            'password':'1234'
}

tutor = { 'email':'tutor@tutor.com',
            'password':'1234'
}

tareas = []

cursos = []

def studentInDB(email, password):
    if (student['email'] == email) and (student['password'] == password):
        return True
    else:
        return False

def tutorInDB(email, password):
    if (tutor['email'] == email) and (tutor['password'] == password):
        return True
    else:
        return False

def get_tareas():
    return tareas

def get_cursos():
    return cursos



# OJo, criterios es una lista de criterios
def crear_tarea(nombre, descripcion, criterios):
    tarea = {'id': random.random() , 'nombre':nombre , 'descripcion': descripcion, 'criterios': criterios }
    tareas.append(tarea)

def crear_curso(nombre, descripcion):
    curso = {'id': random.random(), 'nombre':nombre , 'descripcion': descripcion, 'tareas':[]}
    cursos.append(curso)

# Esto es de prueba
crear_curso("hola mundo", "hola mundo")
    

