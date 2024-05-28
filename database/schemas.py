from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from database.models import *
import sqlalchemy


class Database:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)

    def get_user(self, user_id):
        with self.Session() as session:
            return session.query(User).filter(User.id == user_id).first()

    def get_user_from_email(self, email):
        with self.Session() as session:
            all_users = session.query(User).all()

            # Print the results
            print(f"TODOS LOS USUARIOS: {len(all_users)}")
            return session.query(User).filter(User.email == email).first()

    def get_courses_from_student(self, user):
        with self.Session() as session:
            student = session.query(Student).filter(Student.user_id == user.id).first()
            if student:
                return student.course
            return []

    def get_courses_from_tutor(self, user):
        with self.Session() as session:
            return session.query(Course).filter(Course.tutor_id == user.id).all()

    def is_student(self, user):
        with self.Session() as session:
            return (
                session.query(Student).filter(Student.user_id == user.id).first()
                is not None
            )

    def add_course(self, name, user):
        with self.Session() as session:
            course = Course(name=name, tutor_id=user.id)
            session.add(course)
            session.commit()

    def is_tutor(self, user):
        with self.Session() as session:
            return (
                session.query(Tutor).filter(Tutor.user_id == user.id).first()
                is not None
            )

    def get_course(self, course_id):
        with self.Session() as session:
            return session.query(Course).filter(Course.course_id == course_id).first()

    def get_tasks_from_course(self, course):
        with self.Session() as session:
            return session.query(Task).filter(Task.course_id == course.course_id).all()

    def get_task(self, task_id):
        with self.Session() as session:
            return session.query(Task).filter(Task.task_id == task_id).first()

    def get_criteria_from_task(self, task):
        with self.Session() as session:
            return (
                session.query(Criterion).filter(Criterion.task_id == task.task_id).all()
            )
