-- ANOTACIONES DE CAMBIO DE MYSQL A SQLITE
-- Eliminar las líneas relacionadas con la creación y selección de la base de datos (no es necesario en SQLite)O
-- También debes eliminar la declaración de AUTO_INCREMENT, SQLite maneja esto automáticamente. LOL

-- Creación de tablas
CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Tutor (
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Student (
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Course (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tutor_id INT NOT NULL,
    FOREIGN KEY (tutor_id) REFERENCES Tutor(user_id),
    UNIQUE (name, tutor_id)
);

CREATE TABLE Student_Course (
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES Student(user_id),
    FOREIGN KEY (course_id) REFERENCES Course(id),
    PRIMARY KEY (student_id, course_id)
);

CREATE TABLE Task (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    creation_date DATE,
    deadline_date DATE,
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE Criteria (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    task_id INT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES Task(id),
    UNIQUE (task_id, name)
);

CREATE TABLE Submission (
    id INTEGER PRIMARY KEY,
    date DATE,
    user_id INT NOT NULL,
    task_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Student(user_id),
    FOREIGN KEY (task_id) REFERENCES Task(id),
    UNIQUE (user_id, task_id)
);

CREATE TABLE Review (
    id INTEGER PRIMARY KEY,
    is_pending BOOLEAN NOT NULL DEFAULT 1,
    date DATE,
    reviewer_id INT NOT NULL,
    submission_id INT NOT NULL,
    FOREIGN KEY (reviewer_id) REFERENCES User(id),
    FOREIGN KEY (submission_id) REFERENCES Submission(id),
    UNIQUE (reviewer_id, submission_id)
);

CREATE TABLE Review_Criteria (
    valoracion FLOAT, -- SQLite no tiene FLOAT(3,2), puedes ajustar los límites en la aplicación
    review_id INT NOT NULL,
    criteria_id INT NOT NULL,
    FOREIGN KEY (review_id) REFERENCES Review(id),
    FOREIGN KEY (criteria_id) REFERENCES Criteria(id),
    PRIMARY KEY (review_id, criteria_id)
);
