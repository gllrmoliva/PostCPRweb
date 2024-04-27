import sqlite3
import os

MAIN_PATH = "database"

# Esta función cambia la forma de como SQLite devuelve peticiones fetch
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Connection:

    def connect(self):
        try:
            # Connect to a new SQLite database
            self.connection = sqlite3.connect(MAIN_PATH + "/database.db")
            self.cursor = self.connection.cursor()
            
            # Configura para que las filas se devuelvan como diccionarios
            self.connection.row_factory = dict_factory 
            self.cursor = self.connection.cursor()

        except sqlite3.Error as error:
            print("SQLite Error connecting to the database:", error)
        except Exception as e:
            print("Error connecting to the database:", error)

    def disconnect(self):
        try:
            # Cerrar el cursor y conexión
            if self.connection:
                self.cursor.close()
                self.connection.close()

        except sqlite3.Error as error:
            print("SQLite Error disconnecting the database:", error)
        except Exception as e:
            print("Error disconnecting the database:", e)
        
    def create_tables(self):
        try:
            # Crear tablas usando create_tables.sql
            self.cursor.executescript(open(MAIN_PATH + "/create_tables.sql", 'r').read())
            # Confirmar los cambios
            self.connection.commit()

        except sqlite3.Error as error:
            print("SQLite Error creating tables:", error)
        except Exception as e:
            print("Error creating tables:", e)
    
    def delete_tables(self):
        try:
            # Borrar tablas usando delete_tables.sql
            self.cursor.executescript(open(MAIN_PATH + "/delete_tables.sql", 'r').read())
            # Confirmar los cambios
            self.connection.commit()
            
        except sqlite3.Error as error:
            print("SQLite Error deleting tables:", error)
        except Exception as e:
            print("Error deleting tables:", e)

    # Contract functions
    
    def add_user(self, email, password, name):
        entry_query = "INSERT INTO User (email, password, name) VALUES (?, ?, ?)"
        data = (email, password, name)
        self.cursor.execute(entry_query, data)
        self.connection.commit()

        return self.get_user_from_email(email)
    
    def get_user(self, id):
        entry_query = "SELECT * FROM User WHERE id = ?"
        data = (id, )
        self.cursor.execute(entry_query, data)
        users = self.cursor.fetchall()
   
        if len(users) == 0:
            return None
        return users[0]
    
    def get_user_from_email(self, email):
        entry_query = "SELECT * FROM User WHERE email = ?"
        data = (email, )
        self.cursor.execute(entry_query, data)
        users = self.cursor.fetchall()
   
        if len(users) == 0:
            return None
        return users[0]
    
    def is_student(self, user):
        id = user['id']
        entry_query = "SELECT * FROM Student WHERE user_id = ?"
        data = (id, )
        self.cursor.execute(entry_query, data)
        students = self.cursor.fetchall()
   
        if students == None:
            return False
        if len(students) >= 1:
            return True
        return False
    
    def is_tutor(self, user):
        id = user['id']
        entry_query = "SELECT * FROM Tutor WHERE user_id = ?"
        data = (id, )
        self.cursor.execute(entry_query, data)
        tutors = self.cursor.fetchall()
   
        if tutors == None:
            return False
        if len(tutors) >= 1:
            return True
        return False
    
    def promote_to_student(self, user):
        id = user['id']

        entry_query = "INSERT INTO Student (user_id) VALUES (?)"
        data = (id, )
        self.cursor.execute(entry_query, data)
        self.connection.commit()
    
    def promote_to_tutor(self, user):
        id = user['id']

        entry_query = "INSERT INTO Tutor (user_id) VALUES (?)"
        data = (id, )
        self.cursor.execute(entry_query, data)
        self.connection.commit()
        
    def add_course(self, name, user):
        try:
            tutor_id = user['id']

            entry_query = "INSERT INTO Course (name, tutor_id) VALUES (?, ?)"
            data = (name, tutor_id)

            self.cursor.execute(entry_query, data)
            self.connection.commit()

            return self.get_course_from_pair_name_tutor(name, user)
        except sqlite3.Error as Error:
            print("sqlite3 error: ",Error)
            raise
        except Exception as e:
            print("Exception: ",e)
            raise
        finally:
            self.connection.commit()


    
    def get_course(self, id):
        entry_query = "SELECT * FROM Course WHERE id = ?"
        data = (id, )
        self.cursor.execute(entry_query, data)
        courses = self.cursor.fetchall()
   
        if len(courses) == 0:
            return None
        return courses[0]
    
    def get_courses_from_tutor(self, user):
        tutor_id = user['id']

        entry_query = "SELECT * FROM Course WHERE tutor_id = ?"
        data = (tutor_id, )
        self.cursor.execute(entry_query, data)
        courses = self.cursor.fetchall()
   
        return courses
    
    def add_student_to_course(self, user, course):
        student_id = user['id']
        course_id = course['id']

        entry_query = "INSERT INTO Student_Course (student_id, course_id) VALUES (?, ?)"
        data = (student_id, course_id)
        self.cursor.execute(entry_query, data)
        self.connection.commit()
    
    def get_courses_from_student(self, user):
        student_id = user['id']

        entry_query = "SELECT * FROM Student_Course WHERE student_id = ?"
        data = (student_id, )
        self.cursor.execute(entry_query, data)
        entries = self.cursor.fetchall()

        n = len(entries)
        courses = []
        if n == 0:
            return []
        for i in range(n):
            courses.append(self.get_course(entries[i]['course_id']))
   
        return courses
    
    def get_students_from_course(self, course):
        course_id = course['id']

        entry_query = "SELECT * FROM Student_Course WHERE course_id = ?"
        data = (course_id, )
        self.cursor.execute(entry_query, data)
        entries = self.cursor.fetchall()

        n = len(entries)
        students = []
        if n == 0:
            return []
        for i in range(n):
            students.append(self.get_user(entries[i]['student_id']))
   
        return students

    # Auxiliar functions
    def get_course_from_pair_name_tutor(self, name, user):
        tutor_id = user['id']

        entry_query = "SELECT * FROM Course WHERE name = ? AND tutor_id = ?"
        data = (name, tutor_id)
        self.cursor.execute(entry_query, data)
        courses = self.cursor.fetchall()
   
        if len(courses) == 0:
            return None
        return courses[0]
    
    def fill_tables_with_examples(self):
        try:
            # Rellenar tablas usando example_values.sql
            self.cursor.executescript(open(MAIN_PATH + "/example_values.sql", 'r').read())
            # Confirmar los cambios
            self.connection.commit()

        except sqlite3.Error as error:
            print("SQLite Error filling tables with values:", error)
        except Exception as e:
            print("Error filling tables with values:", e)
