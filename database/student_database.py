from database.model import *
from database.database import Database

from sqlalchemy import (
    create_engine,
    MetaData
)
from sqlalchemy.orm import (
    Session
)

# Se vincula en su iniciación con un estudiante
class StudentDatabase(Database):

    student = None

    # Recibe la id del estudiante a vincular. Devuelve dicho estudiante, o None en caso de que no exista.
    def set_student(self, id):
        self.student = self.get_from_id(Student, id)
        return self.student

    # Da el estado de completitud de una tarea del estudiante vinculado: PENDIENTE, FUERA DE PLAZO, ENVIADO, REVISADO
    def task_completion_status(self, task):
        return self.task_completion_status_of_student(task, self.student)
    
    # Obtiene el puntaje obtenido en un criterio en la entrega del estudiante vinculado
    def criterion_weighted_score(self, criterion):
        return self.criterion_weighted_score_of_student(self, criterion, self.student)

    # Obtiene el puntaje obtenido en una tarea en la entrega del estudiante vinculado
    def task_weighted_score(self, task):
        return self.task_weighted_score_of_student(self, task, self.student)
    
    # Devuelve la entrega (instancia de Submission) de una tarea del estudiante vinculado. Devuelve None si no existe.
    def get_submission(self, task):
        return self.get_submission_of_student(task, self.student)
        