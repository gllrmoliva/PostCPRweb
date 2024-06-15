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
            tutor = session.query(Tutor).filter(Tutor.user_id == user.id).first()
            course = Course(name=name, tutor_id=tutor.tutor_id)
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

    def create_task(self, name, instructions, course):
        with self.Session() as session:
            task = Task(
                name=name, instructions=instructions, course_id=course.course_id
            )
            session.add(task)
            session.commit()

    def get_all_criteria_from_task(self, task_id):
        with self.Session() as session:
            return session.query(Criterion).filter(Criterion.task_id == task_id).all()

    def create_review(self, date, submission, user_id, is_pending=True):
        with self.Session() as session:
            review = Review(
                date=date,
                is_pending=False,
                reviewer_id=user_id,
                submission_id=submission.submission_id,
            )
            session.add(review)
            session.commit()

    def get_criterion_by_name(self, name, task_id):
        with self.Session() as session:
            return (
                session.query(Criterion)
                .filter(Criterion.name == name, Criterion.task_id == task_id)
                .first()
            )

    def get_last_review(self):
        with self.Session() as session:
            return session.query(Review).order_by(Review.review_id.desc()).first()

    def create_review_criterion(self, review_id, criterion_id, score):
        with self.Session() as session:
            review_criterion = ReviewCriterion(
                review_id=review_id,
                criterion_id=criterion_id,
                valoracion=score,
            )
            session.add(review_criterion)
            session.commit()

    def is_review_reviewed(self, review_id, user_id):
        with self.Session() as session:

            review = session.query(Review).filter(Review.review_id == review_id).first()
            print(f"# Is pending: {review.is_pending}\n  ")
            if review is None:
                return False
            else:
                if review.is_pending is True:
                    return False
                elif review.is_pending is False:
                    return True

    def get_reviews_to_review(self, user_id):
        with self.Session() as session:
            return (
                session.query(Review)
                .filter(Review.reviewer_id == user_id and Review.is_pending == True)
                .all()
            )

    def get_tasks_to_review(self, reviews):
        tasks = []
        with self.Session() as session:
            for review in reviews:
                submission = (
                    session.query(Submission)
                    .filter(Submission.submission_id == review.submission_id)
                    .first()
                )
                task = (
                    session.query(Task)
                    .filter(Task.task_id == submission.task_id)
                    .first()
                )
                tasks.append(task)
            return tasks

    def mark_submission_as_reviewed(self, submission, date, teacher_score):
        with self.Session() as session:
            submission_1 = (
                session.query(Submission)
                .filter(Submission.submission_id == submission.submission_id)
                .first()
            )
            submission_1.date = date
            submission_1.reviewed_by_teacher = "REVISADO"
            submission_1.teacher_score = teacher_score
            session.commit()

    def mark_review_as_reviewed(self, submission, user_id):
        with self.Session() as session:
            review = (
                session.query(Review)
                .filter(
                    Review.reviewer_id == user_id,
                    Review.submission_id == submission.submission_id,
                )
                .first()
            )
            review.is_pending = False
            session.commit()

    def get_review(self, review_id):
        with self.Session() as session:
            return session.query(Review).filter(Review.review_id == review_id).first()

    def get_submission_by_review(self, review_id):
        with self.Session() as session:
            submission_id = (
                session.query(Review).filter(Review.review_id == review_id).first()
            ).submission_id
            return (
                session.query(Submission)
                .filter(Submission.submission_id == submission_id)
                .first()
            )

    def get_submissions_from_task(self, task):
        with self.Session() as session:
            return (
                session.query(Submission)
                .filter(Submission.task_id == task.task_id)
                .all()
            )

    def get_name_from_student(self, student_id):
        with self.Session() as session:
            student = (
                session.query(Student).filter(Student.student_id == student_id).first()
            )
            user = session.query(User).filter(User.id == student.user_id).first()
            return user.name

    def get_submission(self, submission_id):
        with self.Session() as session:
            return (
                session.query(Submission)
                .filter(Submission.submission_id == submission_id)
                .first()
            )

    def get_review_by_submission(self, submission_id, user_id):
        with self.Session() as session:
            return (
                session.query(Review)
                .filter(
                    Review.submission_id == submission_id, Review.reviewer_id == user_id
                )
                .first()
            )

    def get_all_reviews_from_task_and_student(self, task_id, student_id):
        with self.Session() as session:
            submission = (
                session.query(Submission)
                .filter(
                    Submission.task_id == task_id, Submission.student_id == student_id
                )
                .first()
            )
            return (
                session.query(Review)
                .filter(Review.submission_id == submission.submission_id)
                .all()
            )
