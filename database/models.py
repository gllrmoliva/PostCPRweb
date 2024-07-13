from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    UniqueConstraint,
    Boolean,
    Date,
    Float,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker,
    Mapped,
    mapped_column,
)

db_url = "sqlite:///database/databaseA.db"

engine = create_engine(db_url, echo=True)


Base = declarative_base()


class StudentCourse(Base):
    __tablename__ = "student_course"
    sc_id = Column(Integer, primary_key=True)
    student_id = Column("student_id", Integer, ForeignKey("student.student_id"))
    course_id = Column("course_id", Integer, ForeignKey("course.course_id"))


class TaskCourse(Base):
    __tablename__ = "task_course"
    tc_id = Column(Integer, primary_key=True)
    task_id = Column("task_id", Integer, ForeignKey("task.task_id"))
    course_id = Column("course_id", Integer, ForeignKey("course.course_id"))


class ReviewCriterion(Base):
    __tablename__ = "review_criterion"
    rc_id = Column(Integer, primary_key=True)
    valoracion = Column(Float)
    review_id = Column("review_id", Integer, ForeignKey("review.review_id"))
    criterion_id = Column("criterion_id", Integer, ForeignKey("criterion.criterion_id"))


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    tutor = relationship("Tutor", back_populates="user", uselist=False)
    student = relationship("Student", back_populates="user", uselist=False)
    review = relationship("Review")


class Tutor(Base):
    __tablename__ = "tutor"
    tutor_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="tutor")
    course = relationship("Course", back_populates="tutor", uselist=False)


class Student(Base):
    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="student")
    course = relationship(
        "Course", secondary="student_course", back_populates="student"
    )


class Course(Base):
    __tablename__ = "course"
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    tutor_id = Column(Integer, ForeignKey("tutor.tutor_id"), nullable=False)
    tutor = relationship("Tutor", back_populates="course")
    __table_args__ = (UniqueConstraint("name", "tutor_id"),)
    student = relationship(
        "Student", secondary="student_course", back_populates="course"
    )
    task = relationship("Task", secondary="task_course", back_populates="course")


class Review(Base):
    __tablename__ = "review"
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    is_pending = Column(Boolean, nullable=False, default=True)
    date = Column(Date)
    reviewer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User")
    submission_id = Column(
        Integer, ForeignKey("submission.submission_id"), nullable=False
    )
    submission = relationship("Submission")
    criterion = relationship(
        "Criterion", secondary="review_criterion", back_populates="review"
    )


class Submission(Base):
    __tablename__ = "submission"
    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    student_id = Column(Integer, ForeignKey("student.student_id"), nullable=False)
    student = relationship("Student")
    review = relationship("Review")
    task_id = Column(Integer, ForeignKey("task.task_id"), nullable=False)
    task = relationship("Task")
    url = Column(String)
    reviewed_by_teacher = Column(String, nullable = False, default = "PENDIENTE")
    teacher_score = Column(Integer, nullable = True, default = None)
    __table_args__ = (UniqueConstraint("student_id", "task_id"),)


class Criterion(Base):
    __tablename__ = "criterion"
    criterion_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    review = relationship(
        "Review", secondary="review_criterion", back_populates="criterion"
    )
    task_id = Column(Integer, ForeignKey("task.task_id"), nullable=False)
    task = relationship("Task")
    __table_args__ = (UniqueConstraint("name", "task_id"),)


class Task(Base):
    __tablename__ = "task"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    instructions = Column(String)
    creation_date = Column(Date)
    deadline_date = Column(Date)
    criterion = relationship("Criterion", back_populates="task", uselist=False)
    submission = relationship("Submission", back_populates="task", uselist=False)
    course_id = Column(Integer, ForeignKey("course.course_id"), nullable=False)
    course = relationship("Course")
    __table_args__ = (UniqueConstraint("name", "course_id"),)
    course = relationship("Course", secondary="task_course", back_populates="task")


Base.metadata.create_all(engine)
