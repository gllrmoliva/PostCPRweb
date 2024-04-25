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

def get_curso(id):
    for curso in cursos:
        if curso['id'] == id:
            return curso

def get_tarea(id):
    for tarea in tareas:
        if tarea['id'] == id:
            return tarea

# OJo, criterios es una lista de criterios
def crear_tarea(idcurso, nombre, descripcion, criterios):
    tarea = {'id': int(random.random()*1000) ,'course':idcurso, 'nombre':nombre , 'descripcion': descripcion, 'criterios': criterios }
    tareas.append(tarea)

def crear_curso(nombre, descripcion):
    curso = {'id': int(random.random()*1000), 'nombre':nombre , 'descripcion': descripcion, 'tareas':[]}
    cursos.append(curso)

# Esto es de prueba
crear_curso("hola mundo", "hola mundo")
    

