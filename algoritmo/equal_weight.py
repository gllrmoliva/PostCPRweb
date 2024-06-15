from database import models
from database.functions import Database
from database.models import engine
from datetime import date
import random


class Equal_Weight:
    students = []
    task = None
    database = Database(engine)

    def __init__(self, students, task):
        self.students = students
        self.task = task

    def create_reviews(self):
        for student in self.students:
            submission = self.database.get_submission_by_user_and_task(
                student.student_id, self.task.task_id
            )
            for i in range(3):
                reviewer = random.choice(self.students)
                while reviewer.student_id == student.student_id:
                    reviewer = random.choice(self.students)

    def final_review(self):
        for student in self.students:
            reviews = self.database.get_all_reviews_from_task_and_student(
                task_id=self.task.task_id, student_id=student.student_id
            )
