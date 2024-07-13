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
    
    # Obtiene el puntaje obtenido en un criterio en la entrega de un estudiante
    # TODO Reemplazar con el algoritmo cuando exista, actualmente como placeholder se calcula el promedio de las revisiones
    def criterion_score(self, criterion):

        sum = 0

        # Obtenemos la entrega del estudiante
        submission = self.get_submission(criterion.task)
        if (submission == None): return 0

        # Por cada revisión de esa entrega
        for review in submission.reviews:
            # Accedemos a las revisiones de los criterios
            for criterion_review in review.criterion_reviews:
                # Y buscamos las revisiones-criterio que hablen del criterio que nos interesa
                if criterion_review.criterion == criterion:

                    sum += criterion_review.score
        
        # Obtenemos el promedio
        n = len(submission.reviews)
        if n == 0: return 0

        return sum / n

    # Obtiene el puntaje obtenido en una tarea en la entrega de un estudiante
    # TODO Reemplazar con el algoritmo cuando exista, actualmente como placeholder se calcula el promedio de las revisiones
    def task_score(self, task):

        sum = 0

        # Sumamos el puntaje obtenido en cada criterio
        for criterion in task.criteria:
            sum += self.criterion_score(criterion)
        
        return sum
    
    # Devuelve la entrega (instancia de Submission) de una tarea del estudiante. Devuelve None si no existe.
    def get_submission(self, task):
        output = None
        for submission in task.submissions:
            if submission in self.student.submissions:
                output = submission
        if output == None:
            print("Student hasn't submitted the task yet")
        return output
        