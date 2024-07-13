import database

database.init()
database.insert_default_values()
database.commit_changes()
database.close()