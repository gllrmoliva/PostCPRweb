import heapq
from database.model import Criterion, Submission, Review, Task, CriterionReview
from statistics import pstdev, fmean

_DEBUG_CONFLICTSORT = True # yea

# -- Funciones acopladas a implementación de la base de datos (actualmente SQLAlchemy) --

def get_score_for_criterion(tg_crit: Criterion, rev: Review):
    for rev_crit in rev.criterion_reviews:
        if tg_crit.id == rev_crit.criterion_id:
            return rev_crit.score

def get_conflictsorted_submissions(some_task: Task):
    pq: heapq[[float, Submission]] = []                         # Priority queue cuya key es el nivel de conflicto de una ``Submission``.
    task_criteria: list[Criterion] = some_task.criteria         # Se asume que está en el mismo orden que la lista de ``criterion_reviews`` de un ``Review``
    task_submissions: list[Submission] = some_task.submissions  # Entregas no ordenadas
    task_criteria_weights: list[float] = []                     # Lista de pesos de cada criterio en la tarea, en este caso representados por los puntajes máximos de cada criterio. 
    ret_val: list[Submission] = []                              # Lista de ``Submission``s retornada

    # Inserción de puntajes máximos de criterios a una lista
    for criterion in task_criteria:
        task_criteria_weights.append(criterion.max_score)

    if _DEBUG_CONFLICTSORT:
        print("Task name: ")
        print(some_task.name)
        print("Criteria: ") 
        for j in range(len(task_criteria)):
            print(task_criteria[j].name)
        print()
        print("Submissions: ")
        for j in range(len(task_submissions)):
            print("Entrega de " + task_submissions[j].student.name)
        print()
        print("Criteria Weights: ")
        for j in range(len(task_criteria_weights)):
            print(task_criteria_weights[j])
        print()

    # TODO: Las revisiones iteradas no poseen el mismo orden de criterios en sus arreglos ``criterion_reviews``. Reescribir el loop para acomodar esto.
    # Loop principal: Determinación de "nivel de conflicto" (o discordancia) presente entre las revisiones de cada entrega
    for submission in task_submissions:
        sub_conflict_level: float = 0
        sub_reviews: list[Review] = submission.reviews          # Lista de coevaluaciones realizadas a esta entrega
        sub_criteria_review_stdev: list[float] = []             # Estructura auxiliar: Lista donde cada valor es la desviación estándar poblacional entre los puntajes asignados a un mismo criterio.
        scores_for_criterion: list[float] = []              # Estructura auxiliar: Puntajes asignados por distintos Review a un mismo criterio de esta entrega
        
        if _DEBUG_CONFLICTSORT:
            print("ITERANDO ENTREGA DE: " + submission.student.name)
            print("======================================")

        # El sistema actualmente no maneja nivel de conflicto para entregas que poseen una única coevaluación.
        if len(sub_reviews) > 1:
            # Se busca calcular la desviación estándar entre los puntajes que las coevaluaciones asignaron a un criterio. Esto se repite para cada criterio de la tarea.
            for criterion in task_criteria:
                for j in range(len(sub_reviews)):
                    scores_for_criterion.append(get_score_for_criterion(criterion, sub_reviews[j]))
                sub_criteria_review_stdev.append(pstdev(scores_for_criterion))
                if _DEBUG_CONFLICTSORT:
                    print("Criterio: " + criterion.name + "; Desviación estándar: " + str(pstdev(scores_for_criterion)))
                scores_for_criterion.clear()

            sub_conflict_level += fmean(sub_criteria_review_stdev, task_criteria_weights)
            t: tuple = [sub_conflict_level, submission] # heapq siempre ordena usando el primer valor
            heapq.heappush(pq, t)
        else:
            continue
        if _DEBUG_CONFLICTSORT:
            print("Nivel de conflicto: " + str(sub_conflict_level))

    # Completando el heapsort, insertar las entregas por orden ascendente de conflicto a una nueva lista.
    for i in range(len(pq)):
        sub: Submission = (heapq.heappop(pq))[1]
        ret_val.append(sub)
    
    # Devolver la lista con discordancia de mayor a menor
    return ret_val.reverse()