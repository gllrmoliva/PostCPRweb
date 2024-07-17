from .context import database
from database.database import *

# Valores por defecto para testear cosas
def insert_default_values(database: Database):
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
    jack = Student(email="jack@stu.com", password="1234", name="Jack Trades")

    fisica.students.append(jack)
    quimica.students.append(jack)

    # Pedro, juan y diego: Estan en fisica
    pedro = Student(email="pedro@stu.com", password="1234", name="Pedro Pérez")
    juan = Student(email="juan@stu.com", password="1234", name="Juan Juárez")
    diego = Student(email="diego@stu.com", password="1234", name="Diego Díaz")

    fisica.students.extend([pedro, juan, diego])

    # Mendel: Esta en biologia
    mendel = Student(email="mendel@stu.com", password="efgh", name="Gregor Mendel") # ¡Contraseña distinta!

    biologia.students.append(mendel)

    # En fisica hay tres tareas:
    tarea_f1 = Task(name="Tarea 1: Posición", instructions="Ubicación en el espacio", course=fisica)
    criterio_f1_1 = Criterion(name="Derivada", description="Calcular la derivada de la posición", max_score=1.0, task=tarea_f1)
    criterio_f1_2 = Criterion(name="Segunda derivada", description="Calcular la segunda derivada de la posición", max_score=2.0, task=tarea_f1)
    criterio_f1_3 = Criterion(name="Tercera derivada", description="Calcular la tercera derivada de la posición", max_score=3.0,task=tarea_f1)

    tarea_f2 = Task(name="Tarea 2: Velocidad", instructions="Cambio de posición en el tiempo", course=fisica)
    criterio_f2_1 = Criterion(name="Derivada", description="Calcular la derivada de la velocidad", max_score=1.0, task=tarea_f2)
    criterio_f2_2 = Criterion(name="Segunda derivada", description="Calcular la segunda derivada de la velocidad", max_score=2.0, task=tarea_f2)

    tarea_f3 = Task(name="Tarea 3: Aceleración", instructions="Cambio de velocidad en el tiempo", course=fisica)
    criterio_f3_1 = Criterion(name="Derivada", description="Calcular la derivada de la aceleración", max_score=1.0, task=tarea_f3)

    # En quimica hay una tarea:
    tarea_q = Task(name="Laboratorio 1", instructions="Informe del laboratorio de termofluidos", course=quimica)
    criterio_q_1 = Criterion(name="Balance de masa", description="Se realiza correctamente el balance de masa", max_score=2.0, task=tarea_q)
    criterio_q_2 = Criterion(name="Balance de energía", description="Se realiza correctamente el balance de energía", max_score=2.0, task=tarea_q)

    # En biologia no hay tareas

    ## Jack hizo las dos primeras tareas de física:
    entrega_jack_1 = Submission(url="www.entrega_de_jack_primera_tarea_de_fisica.com", student=jack, task=tarea_f1)
    entrega_jack_2 = Submission(url="www.entrega_de_jack_segunda_tarea_de_fisica.com", student=jack, task=tarea_f2)

    ## Pedro, Juan y Diego revisaron la entrega de Jack de la primera tarea de física:
    # Pedro le puso el puntaje máximo en todo
    revision_pedro_a_jack = Review(submission=entrega_jack_1, reviewer=pedro)
    r1_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_pedro_a_jack, score=1.0)
    r1_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_pedro_a_jack, score=2.0)
    r1_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_pedro_a_jack, score=3.0)
    revision_pedro_a_jack.is_pending = False

    # Juan le puso el puntaje minimo en todo
    revision_juan_a_jack = Review(submission=entrega_jack_1, reviewer=juan)
    r2_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_juan_a_jack, score=0.0)
    r2_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_juan_a_jack, score=0.0)
    r2_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_juan_a_jack, score=0.0)
    revision_juan_a_jack.is_pending = False

    # Diego puso puntaje maximo en el primer criterio, la mitad en el segundo, el minimo en el tercero
    revision_diego_a_jack = Review(submission=entrega_jack_1, reviewer=diego)
    r3_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_diego_a_jack, score=1.0)
    r3_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_diego_a_jack, score=1.0)
    r3_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_diego_a_jack, score=0.0)
    revision_diego_a_jack.is_pending = False

    ## Entrega de Pedro de la primera tarea de Física, se asignan reviews con "discordancia mínima"
    entrega_pedro = Submission(url="www.entrega_de_pedro_primera_tarea_de_fisica.com", student=pedro, task=tarea_f1)
    # Revision de Jack a Pedro
    revision_jack_a_pedro = Review(submission=entrega_pedro, reviewer=jack)
    r4_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_jack_a_pedro, score=0.5)
    r4_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_jack_a_pedro, score=0.0)
    r4_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_jack_a_pedro, score=3.0)
    revision_jack_a_pedro.is_pending = False

    # Revision de Juan a Pedro
    revision_juan_a_pedro = Review(submission=entrega_pedro, reviewer=juan)
    r5_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_juan_a_pedro, score=1.0)
    r5_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_juan_a_pedro, score=0.0)
    r5_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_juan_a_pedro, score=3.0)
    revision_juan_a_pedro.is_pending = False

    # Revision de Diego a Pedro
    revision_diego_a_pedro = Review(submission=entrega_pedro, reviewer=diego)
    r6_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_diego_a_pedro, score=0.0)
    r6_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_diego_a_pedro, score=0.0)
    r6_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_diego_a_pedro, score=3.0)
    revision_diego_a_pedro.is_pending = False

    ## Entrega de Diego de la primera tarea de Física, discordancia "mediana"
    entrega_diego = Submission(url="www.entrega_de_diego_primera_tarea_de_fisica.com", student=diego, task=tarea_f1)
    # Revision de Jack a diego
    revision_jack_a_diego = Review(submission=entrega_diego, reviewer=jack)
    r4_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_jack_a_diego, score=0.0)
    r4_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_jack_a_diego, score=1.0)
    r4_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_jack_a_diego, score=0.0)
    revision_jack_a_diego.is_pending = False

    # Revision de Juan a diego
    revision_juan_a_diego = Review(submission=entrega_diego, reviewer=juan)
    r5_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_juan_a_diego, score=0.0)
    r5_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_juan_a_diego, score=0.0)
    r5_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_juan_a_diego, score=3.0)
    revision_juan_a_diego.is_pending = False

    # Revision de Pedro a diego
    revision_pedro_a_diego = Review(submission=entrega_diego, reviewer=pedro)
    r6_cr1 = CriterionReview(criterion=criterio_f1_1, review=revision_pedro_a_diego, score=1.0)
    r6_cr2 = CriterionReview(criterion=criterio_f1_2, review=revision_pedro_a_diego, score=2.0)
    r6_cr3 = CriterionReview(criterion=criterio_f1_3, review=revision_pedro_a_diego, score=1.5)
    revision_pedro_a_diego.is_pending = False

    ## Juan hizo la primera tarea de fisica y Jack tiene que revisarla
    entrega_juan = Submission(url="www.entrega_de_juan_primera_tarea_de_fisica.com", student=juan, task=tarea_f1)
    revision_jack_a_juan = Review(submission=entrega_juan, reviewer=jack)

    # Agregamos todo a la base de datos
    # ¡Ojo! Por comportamiento de "cascada" basta con ingresar un elemento el cual recursivamente exista una relación con el resto.
    database._session.add(jack)
    database._session.add(biologia)

if __name__ == "__main__":
    db = Database()
    db.init()
    db.clear()
    insert_default_values(db)
    db.commit_changes()
    db.close()
    