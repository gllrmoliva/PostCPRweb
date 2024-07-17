from .context import database
from database.database import *
from trustsystem.PCPRtrustrank import get_conflictsorted_submissions

# FIXME: esto en realidad no crea una db nueva, instancia un objeto Database que está modificando los mismos datos de ./database/database_0.db (oops)
def create_test_db(database: Database):
    database.init()
    

def conlvl_sort_test():
    db = Database()
    create_test_db(db)
    test_task: Task = db.get_from_id(Task, 1)
    get_conflictsorted_submissions(test_task)

conlvl_sort_test()