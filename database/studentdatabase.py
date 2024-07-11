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

    # Da el estado de completitud de una tarea del estudiante: PENDIENTE, ENVIADA, REVISADA
    def task_completion_status(self, task):
        status = "PENDIENTE"
        for submission in task.submissions:
            if submission in self.student.submissions:
                if len(submission.reviews) == 0:
                    status = "ENVIADO"
                else:
                    status = "REVISADO"
        return status
    
    # Devuelve la entrega (instancia de Submission) de una tarea del estudiante. Devuelve None si no existe.
    def get_submission(self, task):
        output = None
        for submission in task.submissions:
            if submission in self.student.submissions:
                output = submission
        if output == None:
            print("Student hasn't submitted the task yet")
        return output
        