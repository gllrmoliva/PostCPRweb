import heapq
from database.model import Criterion, Submission, Review, Task, CriterionReview
from statistics import pstdev, fmean, quantiles

_DEBUG_CONFLICTSORT = False # yea

# -- Funciones acopladas a implementación de la base de datos (actualmente SQLAlchemy) --

def get_score_for_criterion(tg_crit: Criterion, rev: Review):
    for rev_crit in rev.criterion_reviews:
        if tg_crit.id == rev_crit.criterion_id:
            return rev_crit.score

def get_conflictsorted_submissions(some_task: Task):
    """Genera una lista de instancias de ``Submission`` ordenadas según el "grado de discordancia" presente en ellas, de mayor a menor.
    El grado de discordancia es un ``float`` que representa cuánto difieren el puntaje asignado por las coevaluaciones hechas a una misma entrega.

    Args:
        some_task (Task): Instancia de una tarea con entregas ya coevaluadas

    Returns:
        (list[Submission]): Lista de entregas ordenada por grado de discordancia.
    """    
    pq: heapq[[float, Submission]] = []                         # Priority queue cuya key es el nivel de conflicto de una ``Submission``.
    task_criteria: list[Criterion] = some_task.criteria         # Se asume que está en el mismo orden que la lista de ``criterion_reviews`` de un ``Review``
    task_submissions: list[Submission] = some_task.submissions  # Entregas no ordenadas
    task_criteria_weights: list[float] = []                     # Lista de pesos de cada criterio en la tarea, en este caso representados por los puntajes máximos de cada criterio. 
    ret_val: list[Submission] = []                              # Lista de ``Submission``s retornada
    task_submission_clevels: list[float] = []

    # Inserción de puntajes máximos de criterios a una lista
    for criterion in task_criteria:
        task_criteria_weights.append(criterion.max_score)

    if _DEBUG_CONFLICTSORT:
        print("Task name: ")
        print(some_task.name)
        print()
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

    # Loop principal: Determinación de "nivel de conflicto" (o discordancia) presente entre las revisiones de cada entrega
    for submission in task_submissions:
        sub_conflict_level: float = 0
        sub_reviews: list[Review] = submission.reviews          # Lista de coevaluaciones realizadas a esta entrega
        sub_criteria_review_stdev: list[float] = []             # Estructura auxiliar: Lista donde cada valor es la desviación estándar poblacional entre los puntajes asignados a un mismo criterio.
        scores_for_criterion: list[float] = []              # Estructura auxiliar: Puntajes asignados por distintos Review a un mismo criterio de esta entrega

        # El sistema actualmente no maneja nivel de conflicto para entregas que poseen una única coevaluación.
        if len(sub_reviews) > 1:
            # Se busca calcular la desviación estándar entre los puntajes que las coevaluaciones asignaron a un criterio. Esto se repite para cada criterio de la tarea.
            for criterion in task_criteria:
                for j in range(len(sub_reviews)):
                    scores_for_criterion.append(get_score_for_criterion(criterion, sub_reviews[j]))
                sub_criteria_review_stdev.append(pstdev(scores_for_criterion))
                if _DEBUG_CONFLICTSORT:
                    print("Entrega de: " + submission.student.name + "; Criterio: " + criterion.name + "; Desviación estándar: " + str(pstdev(scores_for_criterion)))
                scores_for_criterion.clear()

            sub_conflict_level += fmean(sub_criteria_review_stdev, task_criteria_weights)
            t: tuple = [sub_conflict_level, submission] # heapq siempre ordena usando el primer valor
            heapq.heappush(pq, t)
        else:
            continue

    # Inserción a ret_val de las entregas por orden ascendente de conflicto
    for i in range(len(pq)):
        pq_tuple: tuple[float, Submission] = heapq.heappop(pq)
        task_submission_clevels.append(pq_tuple[0])
        ret_val.append(pq_tuple[1])
        if _DEBUG_CONFLICTSORT:
            print(pq_tuple[1].student.name +  "; Nivel de conflicto: " + str(pq_tuple[0]))

    # Construcción de un arreglo con los deciles (n = 10) de la distribución de niveles de conflicto. Esto puede ayudar a clasificar los valores ``float`` a algo más utilizable por el front-end del sitio web (como agrupaciones de discordancia BAJA, MEDIA, ALTA?)
    # Sin embargo, siguiendo la documentación del módulo statistics, es recomendado que el largo del iterable (task_submission_clevels) sea mayor a n.
    # Además, para lograr esta clasificación, es necesario encontrar un valor de nivel de discordancia máximo, y que este sea el valor en el decil 10.
    # Realizamos esta última tarea con la desigualdad de Popoviciu para varianzas.
    max_clevel: float = 0.0
    max_criteria_stdev: list[float] = []
    for i in range(len(task_criteria_weights)):
        max_criteria_stdev.append(0.5*(task_criteria_weights[i] - 0))

    max_clevel = fmean(max_criteria_stdev, task_criteria_weights)
    task_submission_clevels.append(max_clevel)
    
    if len(task_submission_clevels) < 10:
        clevel_quantiles = quantiles(task_submission_clevels, n=len(task_submission_clevels))
    else:
        clevel_quantiles = quantiles(task_submission_clevels, n=10)

    # DEBUGPRINT: deciles para la variable aleatoria X: Nivel de conflicto
    if _DEBUG_CONFLICTSORT:
        for i in range(len(clevel_quantiles)):
            print("Decile " + str(i) + ": " + str(clevel_quantiles[i]))


    # Devolver la lista de Submissions, con discordancia descendiente.
    return ret_val.reverse()