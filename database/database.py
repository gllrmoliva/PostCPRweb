from database.model import *

from sqlalchemy import (
    create_engine,
    MetaData,
    select,
    exc
)
from sqlalchemy.orm import (
    Session
)

class IntegrityException(Exception):
    pass


# Clase con métodos que acceden a la base de datos a traves de la lógica orientada a objetos de SQLAlchemy
class Database:

    def init(self):
        self._engine = create_engine("sqlite:///database/database_0.db", echo=False, future=True)
        Base.metadata.create_all(self._engine)
        self._session = Session(self._engine)

    def close(self):
        self._session.close()

    # Añade una instancia a la base de datos. IMPORTANTE: No hace commit automaticamente.
    def add(self, entry):
        self._session.add(entry)
    
    # Añade un conjunto de instancias a la base de datos. IMPORTANTE: No hace commit automaticamente.
    def add_all(self, entries):
        self._session.add_all(entries)
    
     # Elimina una instancia de la base de datos. IMPORTANTE: No hace commit automaticamente.
    def delete(self, entry):
        self._session.delete(entry)
    
    # Elimina un conjunto de instancias de la base de datos. IMPORTANTE: No hace commit automaticamente.
    def delete_all(self, entries):
        for entry in entries:
            self.delete(entry)

    # Cualquier cambio primero es ingresado en un espacio intermedio (Session). Con este metodo se ingresan a la base de datos.
    def commit_changes(self):
        try:
            self._session.commit()
        except exc.IntegrityError as e:
            raise IntegrityException(e._message)
        except Exception as e:
            raise e
    
    # Desecha los cambios no commiteados. Muy util si ocurre una excepción al hacer commit.
    def rollback_changes(self):
        self._session.rollback()

    def clear(self):
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    # Devuelve una instancia de User en caso exitoso. Devuelve None en caso de fallo.
    def login_student(self, email, password):
        student = self._session.query(Student).where(Student.email == email, Student.password == password).first()
        if (student == None):
            print("Student login failed")
            return None
        else:
            return student

    # Devuelve una instancia de User en caso exitoso. Devuelve None en caso de fallo.
    def login_tutor(self, email, password):
        tutor = self._session.query(Tutor).where(Tutor.email == email, Tutor.password == password).first()
        if (tutor == None):
            print("Tutor login failed")
            return None
        else:
            return tutor

    # Devuelve instancia de una clase a partir de su id
    def get_from_id(self, Type, id):
        instance = self._session.query(Type).where(Type.id == id).first()    
        if (instance == None):
            print(f"Getting {Type.__name__} from id failed")
            return None
        else:
            return instance
    
    # Devuelve todas las intancias de una clase
    def get_all(self, Type):
        instances = self._session.scalars(select(User).order_by(User.type)).all()
        if (len(instances) == 0):
            print(f"Getting all instances of {Type.__name__} failed")
            return None
        else:
            return instances
    
    # Suma el puntaje de todos los criterios de una tarea
    def task_max_score(self, task):
        max_score = 0
        for criterion in task.criteria:
            max_score += criterion.max_score
        return max_score