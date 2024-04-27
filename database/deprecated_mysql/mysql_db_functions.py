import mysql.connector

class Connection:
    # Initialize and terminate connection

    def connect(self):
        try:
            # Connect to MySQL server
            self.connection = mysql.connector.connect(
                host="localhost",       # Hostname where MySQL server is running
                user="root",            # MySQL username
                password="root",        # MySQL password
                database="test"         # Name of the database you created
            )

            # Create a cursor object to execute SQL queries
            self.cursor = self.connection.cursor(dictionary=True)
    
        except mysql.connector.Error as error:
            print("Error connecting to the database:", error)
        except Exception as e:
            print("Error connecting to the database", e)

    def disconnect(self):
        try:
            # Close the cursor and connection
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
    
        except mysql.connector.Error as error:
            print("Error disconnecting the database:", error)
        except Exception as e:
            print("Error disconnecting the database", e)

    # Contract functions
    
    def add_user(self, email, password, name):
        entry_query = "INSERT INTO User (email, password, name) VALUES (%s, %s, %s)"
        data = (email, password, name)
        self.cursor.execute(entry_query, data)
        self.connection.commit()

        return self.get_user_from_email(email)
    
    def get_user(self, id):
        entry_query = "SELECT * FROM User WHERE id = %s"
        data = (id, )
        self.cursor.execute(entry_query, data)
        users = self.cursor.fetchall()
   
        if len(users) == 0:
            return None
        return users[0]
    
    def get_user_from_email(self, email):
        entry_query = "SELECT * FROM User WHERE email = %s"
        data = (email, )
        self.cursor.execute(entry_query, data)
        users = self.cursor.fetchall()
   
        if len(users) == 0:
            return None
        return users[0]
    
    def is_student(self, user):
        id = user['id']
        entry_query = "SELECT * FROM Student WHERE user_id = %s"
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
        entry_query = "SELECT * FROM Tutor WHERE user_id = %s"
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

        entry_query = "INSERT INTO Student (user_id) VALUES (%s)"
        data = (id, )
        self.cursor.execute(entry_query, data)
        self.connection.commit()
    
    def promote_to_tutor(self, user):
        id = user['id']

        entry_query = "INSERT INTO Tutor (user_id) VALUES (%s)"
        data = (id, )
        self.cursor.execute(entry_query, data)
        self.connection.commit()
        
    def add_course(self, name, user):
        tutor_id = user['id']

        entry_query = "INSERT INTO Course (name, tutor_id) VALUES (%s, %s)"
        data = (name, tutor_id)
        self.cursor.execute(entry_query, data)
        self.connection.commit()

        return self.get_course_from_pair_name_tutor(name, user)
    
    def get_course(self, id):
        entry_query = "SELECT * FROM Course WHERE id = %s"
        data = (id, )
        self.cursor.execute(entry_query, data)
        courses = self.cursor.fetchall()
   
        if len(courses) == 0:
            return None
        return courses[0]
    
    def get_courses_from_tutor(self, user):
        tutor_id = user['id']

        entry_query = "SELECT * FROM Course WHERE tutor_id = %s"
        data = (tutor_id, )
        self.cursor.execute(entry_query, data)
        courses = self.cursor.fetchall()
   
        return courses
    
    def add_student_to_course(self, user, course):
        student_id = user['id']
        course_id = course['id']

        entry_query = "INSERT INTO Student_Course (student_id, course_id) VALUES (%s, %s)"
        data = (student_id, course_id)
        self.cursor.execute(entry_query, data)
        self.connection.commit()
    
    def get_courses_from_student(self, user):
        student_id = user['id']

        entry_query = "SELECT * FROM Student_Course WHERE student_id = %s"
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

        entry_query = "SELECT * FROM Student_Course WHERE course_id = %s"
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

        entry_query = "SELECT * FROM Course WHERE name = %s AND tutor_id = %s"
        data = (name, tutor_id)
        self.cursor.execute(entry_query, data)
        courses = self.cursor.fetchall()
   
        if len(courses) == 0:
            return None
        return courses[0]


# MAIN
c = Connection()
c.connect()
user = c.add_user("john@mail.com", "1234", "John")
print( c.get_user(user['id']) )
print( c.is_student(user))
c.promote_to_student(user)
print( c.is_student(user))
print( c.is_tutor(user))
c.promote_to_tutor(user)
print( c.is_tutor(user))
print( c.get_courses_from_tutor(user))
course1 = c.add_course("calculus", user)
course2 = c.add_course("algebra", user)
print( c.get_courses_from_tutor(user))
c.add_student_to_course(user, course1)
c.add_student_to_course(user, course2)
courses = c.get_courses_from_student(user)
print(courses)
students1 = c.get_students_from_course(course1)
students2 = c.get_students_from_course(course2)
print(students1)
print(students2)
c.disconnect()
