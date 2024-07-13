from model import *

from sqlalchemy import (
    create_engine,
    MetaData
)
from sqlalchemy.orm import (
    Session
)

# Conexión
engine = create_engine("sqlite:///database_0.db", echo=False, future=True)

# Borrar todo
Base.metadata.drop_all(engine)

# Crear esquema
Base.metadata.create_all(engine)

# Abrir sesión
session = Session(engine)

# -- TEST -- #

john = Student(email="john@stu.com", password="1234", name="John")
mike = Student(email="mike@ßstu.com", password="1234", name="Michael")
alice = Tutor(email="alice@tut.com", password="1234", name="Alice")

math = Course(name="Math")
math.tutor = alice
math.students.append(john)
math.students.append(mike)

task = Task(name="Sum", instructions="2+2=?", course=math)
crit1 = Criterion(name="Grammar", task=task)
crit2 = Criterion(name="Puntuality", task=task)

sub = Submission(url="solution.com", student=john, task=task)

review = Review(submission=sub, reviewer=mike)
cr1 = CriterionReview(criterion=crit1, review=review, score=0.9)
cr2 = CriterionReview(criterion=crit2, review=review, score=1.0)

session.add_all([john, alice, math, task, sub, review, cr1, cr2])

session.commit()

session.close()