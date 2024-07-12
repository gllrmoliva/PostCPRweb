from database.model import *

from sqlalchemy import (
    create_engine,
    MetaData
)
from sqlalchemy.orm import (
    Session
)

# Clase con métodos que acceden a la base de datos a traves de la lógica orientada a objetos de SQLAlchemy
class Database:

    def init(self):
        self.engine = create_engine("sqlite:///database/database_0.db", echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def close(self):
        self.session.close()

    # Añade una instancia a la base de datos. IMPORTANTE: No hace commit automaticamente.
    def add(self, entry):
        self.session.add(entry)
    
    # Añade un conjunto de instancias a la base de datos. IMPORTANTE: No hace commit automaticamente.
    def add_all(self, entries):
        self.session.add_all(entries)

    # Cualquier cambio primero es ingresado en un espacio intermedio (Session). Con este metodo se ingresan a la base de datos.
    def commit_changes(self):
        self.session.commit()

    def clear(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    # Devuelve una instancia de User en caso exitoso. Devuelve None en caso de fallo.
    def login_student(self, email, password):
        student = self.session.query(Student).where(Student.email == email, Student.password == password).first()
        if (student == None):
            print("Student login failed")
            return None
        else:
            return student

    # Devuelve una instancia de User en caso exitoso. Devuelve None en caso de fallo.
    def login_tutor(self, email, password):
        tutor = self.session.query(Tutor).where(Tutor.email == email, Tutor.password == password).first()
        if (tutor == None):
            print("Tutor login failed")
            return None
        else:
            return tutor

    # Devuelve instancia de una clase a partir de su id
    def get_from_id(self, Type, id):
        instance = self.session.query(Type).where(Type.id == id).first()    
        if (instance == None):
            print(f"Getting {Type.__name__} from id failed")
            return None
        else:
            return instance
    
    # Suma el puntaje de todos los criterios de una tarea
    def task_max_score(self, task):
        max_score = 0
        for criterion in task.criteria:
            max_score += criterion.max_score
        return max_score
