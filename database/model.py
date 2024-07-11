from __future__ import annotations
from typing import List
from datetime import date

from sqlalchemy import (
    Table,
    Column,
    ForeignKey
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

class Base(DeclarativeBase):
    pass

# -- Tabla asociativa auxiliar --

student_course_association = Table(
    "student_course_table",
    Base.metadata,
    Column("student_id", ForeignKey("student_table.id"), primary_key=True),
    Column("course_id", ForeignKey("course_table.id"), primary_key=True)
)

# -- Clases ORM -- 

# Describe un usuario de la plataforma
class User(Base):
    __tablename__ = "user_table"

    # Atributos no relacionales
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    # Atributos relacionales
    reviews: Mapped[List[Review]] = relationship(back_populates="reviewer")

    # Herencia
    type: Mapped[str]
    __mapper_args__ = {
        "polymorphic_identity": "USER",
        "polymorphic_on": "type",
    }

# Describe un tutor de la plataforma. Es un usuario (Herencia)
class Tutor(User):
    __tablename__ = "tutor_table"

    # Atributos relacionales
    id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    courses: Mapped[List[Course]] = relationship(back_populates="tutor")

    # Herencia
    __mapper_args__ = {
        "polymorphic_identity": "TUTOR",
    }

# Describe un estudiante de la plataforma. Es un usuario (Herencia)
class Student(User):
    __tablename__ = "student_table"

    # Atributos relacionales
    id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
    courses: Mapped[List[Course]] = relationship(secondary=student_course_association, back_populates="students")
    submissions: Mapped[List[Submission]] = relationship(back_populates="student")

    # Herencia
    __mapper_args__ = {
        "polymorphic_identity": "STUDENT",
    }

# Describe un curso
class Course(Base):
    __tablename__ = "course_table"

    # Atributos no relacionales
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    # Atributos relacionales
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutor_table.id"), nullable=False)
    tutor: Mapped[Tutor] = relationship(back_populates="courses")
    students: Mapped[List[Student]] = relationship(secondary=student_course_association, back_populates="courses")
    tasks: Mapped[List[Task]] = relationship(back_populates="course")

# Describe una tarea de un curso. No confundir con una entrega ni revisión
class Task(Base):
    __tablename__ = "task_table"

    # Atributos no relacionales
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    instructions: Mapped[str | None] = mapped_column()
    deadline_date: Mapped[date | None] = mapped_column()

    # Atributos relacionales
    course_id: Mapped[int] = mapped_column(ForeignKey("course_table.id"), nullable=False)
    course: Mapped[Course] = relationship(back_populates="tasks")
    criteria: Mapped[List[Criterion]] = relationship(back_populates="task")
    submissions: Mapped[List[Submission]] = relationship(back_populates="task")

# Describe un criterio de evaluación de una tarea. No confundir con la revisión de un criterio
class Criterion(Base):
    __tablename__ = "criterion_table"

    # Atributos no relacionales
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    # Atributos relacionales
    task_id: Mapped[int] = mapped_column(ForeignKey("task_table.id"), nullable=False)
    task: Mapped[Task] = relationship(back_populates="criteria")

# Describe la entrega de un estudiante de una tarea. No confundir con la revisión de una entrega
class Submission(Base):
    __tablename__ = "submission_table"

    # Atributos no relacionales
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[date | None] = mapped_column()

    # Atributos relacionales
    student_id: Mapped[int] = mapped_column(ForeignKey("student_table.id"), nullable=False)
    student: Mapped[Student] = relationship(back_populates="submissions")
    task_id: Mapped[int] = mapped_column(ForeignKey("task_table.id"), nullable=False)
    task: Mapped[Task] = relationship(back_populates="submissions")
    reviews: Mapped[List[Review]] = relationship(back_populates="submission")

# Describe la revisión de una entrega de una tarea. La evaluación de los criterios se describen en una tabla aparte
class Review(Base):
    __tablename__ = "review_table"

    # Atributos no relacionales
    id: Mapped[int] = mapped_column(primary_key=True)

    # Atributos relacionales
    submission_id: Mapped[int] = mapped_column(ForeignKey("submission_table.id"), nullable=False)
    submission: Mapped[Submission] = relationship(back_populates="reviews")
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), nullable=False)
    reviewer: Mapped[User] = relationship(back_populates="reviews")
    criterion_reviews: Mapped[List[CriterionReview]] = relationship(back_populates="review")

# Describe la evaluación de un criterio en la revisión de una entrega
class CriterionReview(Base):
    __tablename__ = "criterion_review_table"

    # Atributos relacionales
    score: Mapped[float] = mapped_column(nullable=False)

    # Atributos no relacionales
    criterion_id: Mapped[int] = mapped_column(ForeignKey("criterion_table.id"), primary_key=True)
    criterion: Mapped[Criterion] = relationship()
    review_id: Mapped[int] = mapped_column(ForeignKey("review_table.id"), primary_key=True)
    review: Mapped[Review] = relationship(back_populates="criterion_reviews")
