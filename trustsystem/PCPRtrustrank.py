import heapq
from database.model import Criterion, Submission, Review, Task, CriterionReview
from statistics import pstdev

# -- Funciones acopladas a implementación de la base de datos (actualmente SQLAlchemy) --

def get_conflictsorted_submissions(some_task: Task):
    pq: heapq[[float, Submission]] = []                         # Priority queue cuya key es el nivel de conflicto de una ``Submission``.
    ret_val: list[Submission] = []                              # Lista de ``Submission``s retornada
    task_criteria: list[Criterion] = some_task.criteria         # Se asume que está en el mismo orden que la lista de ``criterion_reviews`` de un ``Review``
    task_submissions: list[Submission] = some_task.submissions  # Entregas no ordenadas

    for submission in task_submissions:
        sub_conflict_level: float = 0
        sub_reviews: list[Review] = submission.reviews
        # Importante: Se itera sobre los criterios de Task, asumiendo que cada Review posee el mismo orden de criterios.
        for j in range(len(task_criteria)):
            criterion_scores: list[float] = []
            for review in sub_reviews:
                criterion_scores.append((review.criterion_reviews[j]).score)
            sub_conflict_level += pstdev(criterion_scores)

        t: tuple = [sub_conflict_level, submission] # heapq siempre ordena usando el primer valor
        heapq.heappush(pq, t)

    # Completando el heapsort, insertar las entregas por orden ascendente de conflicto a una nueva lista.
    for i in range(len(pq)):
        sub: Submission = (heapq.heappop(pq))[1]
        ret_val.append(sub)
    
    # Devolver la lista con discordancia de mayor a menor
    return ret_val.reverse()