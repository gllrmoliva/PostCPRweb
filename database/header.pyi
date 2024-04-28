# Este archivo actualmente no afecta en nada al programa y su ejecución
# Su función es proveer de una documentación donde revisar los métodos de la base de datos

# Clase que contiene la conexión con la base de datos
# Cualquier petición a la base de datos es a traves de metodos de esta clase
class Connection:

    ### Métodos generales:
    
    # Conecta la instancia a la base de datos. Obligatorio para llamar cualquier otro método
    def connect(self) -> None: ...
    # Desconecta a la instancia de la base de datos
    def disconnect(self) -> None: ...
    # Crea las tablas de la base de datos. Da error si ya existen.
    def create_tables(self) -> None: ...
    # Elimina las tablas de la base de datos sólo si existen. No da error si no existen.
    def delete_tables(self) -> None: ...


    ### Usuarios, Estudiantes y Profesores:

    # Un usuario es representado por un diccionario
    user = dict
    # Con llaves: 'id', 'email', 'password', 'name'

    # Importante: Un usuario puede ser un estudiante o un profesor:
    # - Estudiante y profesor no son diccionarios aparte.
    # - Existen métodos is_student() y is_tutor() para comprobarlo.
    student = user
    tutor = user

    # Añade un usuario a la base de datos
    def add_user(self, email, password, name) -> user: ...
    # Devuelve un usuario sólo conociendo su id
    def get_user(self, id) -> user: ...
    # Devuelve un usuario sólo conociendo su correo
    def get_user_from_email(self, email) -> user: ...
    # Revisa si un usuario es estudiante
    def is_student(self, user) -> bool: ...
    # Revisa si un usuario es profesor
    def is_tutor(self, user) -> bool: ...
    # Registra a un usuario como estudiante
    def promote_to_student(self, user) -> None: ...
    # Registra a un usuario como profesor
    def promote_to_tutor(self, user) -> None: ...


    ### Cursos:

    # Un curso es representado por un diccionario
    course = dict
    # Con llaves: 'id', 'name', 'tutor_id'
    # - 'tutor_id' es la id de usuario del tutor que administra el curso.

    # Añade un curso a la base de datos. Recibe un usuario profesor
    def add_course(self, name, tutor) -> course: ...
    # Devuelve un curso sólo conociendo su id
    def get_course(self, id) -> course: ...
    # Devuelve la lista de cursos a cargo de un profesor. Recibe el usuario de dicho profesor
    def get_courses_from_tutor(self, tutor) -> list[course]: ...
    # Añade un estudiante a un curso
    def add_student_to_course(self, student, course) -> None: ...
    # Devuelve los cursos a los que pertenece un estudiante
    def get_courses_from_student(self, student) -> list[course]: ...
    # Devuelve los estudiantes que pertenecen a un curso
    def get_students_from_course(self, course) -> list[student]: ...


    ### Tareas:

    # Una tarea es representada por un diccionario
    task = dict
    # Con llaves: 'id', 'name', 'creation_date', 'deadline_date', 'course_id'
    # - Las fechas son texto en formato YYYY-MM-DD
    # - 'course_id' es la id del curso de la tarea.
    # - Por ahora se ignoran 'creation_date' y 'deadline_date'. Siempre valen None
    
    # Añade una tarea a la base de datos. Recibe el curso de la tarea
    def add_task(self, name, course) -> task: ...
    # Devuelve una tarea sólo conociendo su id
    def get_task(self, id) -> task: ...
    # Devuelve la lista de tareas de un curso. Recibe dicho curso como parametro
    def get_tasks_from_course(self, course) -> list[task]: ...


    ### Criterios:

    # Un criterio es representado por un diccionario
    criterion = dict
    # Con llaves: 'id', 'name', 'task_id'
    # - 'task_id' es la id de la tarea correspondiente al criterio.

    # Añada un criterio a la base de datos. Recibe la tarea a la que va a pertenecer el criterio
    def add_criterion(self, name, task) -> criterion: ...
    # Devuelve un criterio sólo conociendo su id
    def get_criterion(self, id) -> criterion: ...
    # Devuelve la lista de criterios de una tarea. Recibe dicha tarea como parametro
    def get_criteria_of_task(self, task) -> list[criterion]: ...


    ### Entregas:

    # Una entrega es representada por un diccionario
    submission = dict
    # Con llaves: 'id', 'date', 'student_id', 'task_id'
    # - Las fechas son texto en formato YYYY-MM-DD
    # - 'student_id' es la id de usuario del estudiante que entregó su tarea.
    # - 'task_id' es la id de la tarea que se entregó.
    # - Por ahora se ignora 'date'. Siempre vale None

    # Añade la entrega de una tarea de un estudiante a la base de datos. Recibe dicha tarea y estudiante
    def add_submission(self, student, task) -> submission: ...
    # Devuelve una tarea sólo conociendo su id
    def get_submission(self, id) -> submission: ...
    # Devuelve la lista de entregas de una tarea que han sido enviadas. Recibe dicha tarea como parametro
    def get_submissions_of_task(self, task) -> list[submission]: ...
    # Devuelve la lista de entregas de ha enviado un estudiante. Recibe dicho estudiante como parametro
    def get_submissions_from_student(self, student) -> list[submission]: ...
    # Revisa si una estudiante ha entregado una tarea. Recibe dicho estudiante y tarea como parametro.
    def exists_submission_of_task_from_student(self, task, student) -> bool: ...
    # Devuelve la entrega de una tarea de un estudiante. Recibe dicho estudiante y tarea como parametro.
    def get_submission_of_task_from_student(self, task, student) -> submission: ...


    ### Métodos auxiliares:
    # Métodos que usados para implementar o probar otros métodos.
    # No tienen mucho uso. Incluidos por si llegan a ser utiles.
    def fill_tables_with_examples(self) -> None: ...
    def get_course_from_pair_name_tutor(self, name, tutor) -> course: ...
    

