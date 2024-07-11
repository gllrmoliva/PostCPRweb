from database.database import Database
from database.model import *

# Valores por defecto para testear cosas
def insert_default_values(database):

    # Hay tres cursos:
    fisica = Course(name="Física")
    quimica = Course(name="Química")
    biologia = Course(name="Biología")

    # Los tres profesores por cada curso, respectivamente:
    newton = Tutor(email = "newton@tut.com", password="1234", name="Isaac Newton")
    curie = Tutor(email="curie@tut.com", password="1234", name="Marie Curie")
    darwin = Tutor(email="darwin@tut.com", password="abcd", name="Charles Darwin")  # ¡Contraseña distinta!

    fisica.tutor = newton
    quimica.tutor = curie
    biologia.tutor = darwin

    # Hay varios alumnos:

    # Jack: Esta en fisica y quimica, no esta en biologia, tiene tareas por hacer, enviadas y revisadas. Tiene revisiones por hacer y hechas.
    jack = Student(email="jack@stu.com", password="1234", name="Jack of all trades")

    fisica.students.append(jack)
    quimica.students.append(jack)

    # Pedro, juan y diego: Estan en fisica
    pedro = Student(email="pedro@stu.com", password="1234", name="Pedro")
    juan = Student(email="juan@stu.com", password="1234", name="Juan")
    diego = Student(email="diego@stu.com", password="1234", name="Diego")

    fisica.students.extend([pedro, juan, diego])

    # Mendel: Esta en biologia
    mendel = Student(email="mendel@stu.com", password="fegh", name="Gregor Mendel") # ¡Contraseña distinta!

    biologia.students.append(mendel)

    # En fisica hay tres tareas:
    tarea_f1 = Task(name="Posición", instructions="Ubicación en el espacio", course=fisica)
    criterio_f1_1 = Criterion(name="Derivada", description="Calcular la derivada de la posición", max_score=1.0, task=tarea_f1)
    criterio_f1_2 = Criterion(name="Segunda derivada", description="Calcular la segunda derivada de la posición", max_score=2.0, task=tarea_f1)
    criterio_f1_3 = Criterion(name="Tercera derivada", description="Calcular la tercera derivada de la posición", max_score=3.0,task=tarea_f1)

    tarea_f2 = Task(name="Velocidad", instructions="Cambio de posición en el tiempo", course=fisica)
    criterio_f2_1 = Criterion(name="Derivada", description="Calcular la derivada de la velocidad", max_score=1.0, task=tarea_f2)
    criterio_f2_2 = Criterion(name="Segunda derivada", description="Calcular la segunda derivada de la velocidad", max_score=2.0, task=tarea_f2)

    tarea_f3 = Task(name="Aceleración", instructions="Cambio de velocidad en el tiempo", course=fisica)
    criterio_f3_1 = Criterion(name="Derivada", description="Calcular la derivada de la aceleración", max_score=1.0, task=tarea_f3)

    # En quimica hay una tarea:
    tarea_q = Task(name="Laboratorio 1", instructions="Informe del laboratorio de termofluidos", course=quimica)
    criterio_q_1 = Criterion(name="Balance de masa", description="Se realiza correctamente el balance de masa", max_score=2.0, task=tarea_q)
    criterio_q_2 = Criterion(name="Balance de energía", description="Se realiza correctamente el balance de energía", max_score=2.0, task=tarea_q)

    # En biologia no hay tareas

    # Jack hizó las dos primeras tareas de física:
    entrega_jack_1 = Submission(url="posicion.cl", student=jack, task=tarea_f1)
    entrega_jack_2 = Submission(url="velocidad.cl", student=jack, task=tarea_f2)

    # Pedro, Juan y Diego revisaron la entrega de Jack de la primera tarea de física:

    # Pedro le puso el puntaje máximo en todo
    revision_pedro_a_jack = Review(submission=entrega_jack_1, reviewer=pedro)
    r1_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_pedro_a_jack, score=1.0)
    r1_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_pedro_a_jack, score=2.0)
    r1_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_pedro_a_jack, score=3.0)
    # Juan le puso el puntaje minimo en todo
    revision_juan_a_jack = Review(submission=entrega_jack_1, reviewer=juan)
    r2_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_juan_a_jack, score=0.0)
    r2_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_juan_a_jack, score=0.0)
    r2_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_juan_a_jack, score=0.0)
    # Diego puso puntaje maximo en el primer criterio, la mitad en el segundo, el minimo en el tercero
    revision_diego_a_jack = Review(submission=entrega_jack_1, reviewer=diego)
    r3_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_diego_a_jack, score=1.0)
    r3_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_diego_a_jack, score=1.0)
    r3_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_diego_a_jack, score=0.0)

    # TODO:
    # Pedro hizo la primera tarea y Jack la revisó
    # Juan hizo la primera tarea y Jack tiene que revisarla
    # Diego hizo la primera tarea y Pedro tiene que revisarla

    # Agregamos todo a la base de datos
    # ¡Ojo! Por comportamiento de "cascada" basta con ingresar un elemento el cual recursivamente exista una relación con el resto.
    database.session.add(jack)
    database.session.add(biologia)

if __name__ == "__main__":
    db = Database()
    db.init()
    db.clear()
    insert_default_values(db)
    db.commit_changes()
    db.close()
    