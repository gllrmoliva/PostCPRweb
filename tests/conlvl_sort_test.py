from .context import database
from database.database import *
from database.example_values import insert_default_values
from trustsystem.PCPRtrustrank import get_conflictsorted_submissions

def create_test_db(database: Database):
    database.init()
    database.clear()
    insert_default_values(database)
    database.commit_changes()
    database.close()

def conlvl_sort_test():
    db = Database()
    create_test_db(db)
    test_task: Task = db.get_from_id(Task, 1)
    print(test_task.name)
    get_conflictsorted_submissions(test_task)
    print("placeholder")

conlvl_sort_test()