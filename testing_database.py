from database import db 
"""
En este archivo se pueden probar las funciones hechas en el modulo database de la app
- Si es que pueden hacer que se añadan datos por defecto a la base de datos estaria 
bueno, así se podrian probar usuarios en el frontend de forma mas sencilla, 
creo que seria buena idea hacerlo en un .sql y ejecutarlo en la creación de Connection
"""

c = db.Connection()
c.connect()
user = c.add_user("john@mail.com", "1234", "John")
print( c.get_user(user['id']) )
print( c.is_student(user))
c.promote_to_student(user)
print( c.is_student(user))
print( c.is_tutor(user))
c.promote_to_tutor(user)
print( c.is_tutor(user))
print( c.get_courses_from_tutor(user))
course1 = c.add_course("calculus", user)
course2 = c.add_course("algebra", user)
print( c.get_courses_from_tutor(user))
c.add_student_to_course(user, course1)
c.add_student_to_course(user, course2)
courses = c.get_courses_from_student(user)
print(courses)
students1 = c.get_students_from_course(course1)
students2 = c.get_students_from_course(course2)
print(students1)
print(students2)
c.disconnect()