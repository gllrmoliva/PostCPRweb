from database import db 
"""
En este archivo se pueden probar las funciones hechas en el modulo database de la app
- Si es que pueden hacer que se añadan datos por defecto a la base de datos estaria 
bueno, así se podrian probar usuarios en el frontend de forma mas sencilla, 
creo que seria buena idea hacerlo en un .sql y ejecutarlo en la creación de Connection
"""

c = db.Connection()
c.connect()

c.delete_tables()
c.create_tables()

c.fill_tables_with_examples()

mail = input("Ingrese su correo de estudiante: ")
try:
    user = c.get_user_from_email(mail)
    courses = c.get_courses_from_student(user)
    for i in range(len(courses)):
        course = courses[i]
        tutor = c.get_user(course['tutor_id'])
        print("Curso:", course['name'], "\tTutor:", tutor['name'])
except Exception as e:
    print(e)


c.disconnect()
