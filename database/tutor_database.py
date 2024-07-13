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
        self.tutor = self.get_from_id(Tutor, id)
        return self.tutor