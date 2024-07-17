from database.model import *
from database.database import Database

from sqlalchemy import (
    create_engine,
    MetaData
)
from sqlalchemy.orm import (
    Session
)

# Se vincula en su iniciación con un tutor
class TutorDatabase(Database):

    tutor = None

    # Recibe la id del tutor a vincular. Devuelve dicho tutor, o None en caso de que no exista.
    def set_tutor(self, id):

        # Para sincronizar con sesiones simultaneas. ¡No es una buena solución!
        self._session.expire_all()
        
        self.tutor = self.get_from_id(Tutor, id)
        return self.tutor
    
    # Busca un estudiante a partir de su correo (Un atributo unico y no nulo)
    #   Este método podria estar perfectamente en la clase padre Database. me esta haciendo reconsiderar cosas
    #   Además se podria hacer perfectamente con una query más génerica
    def get_student_from_email(self, email):
        instance = self._session.query(Student).where(Student.email == email).first()  
        if (instance == None):
            print(f"Getting student from email failed")
            return None
        else:
            return instance