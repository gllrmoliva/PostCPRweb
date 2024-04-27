-- Creación de tablas

CREATE TABLE User (
    -- Atributos no relacionales 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE Tutor (
    -- Atributos relacionales 
    user_id INTEGER PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Student (
    -- Atributos relacionales
    user_id INTEGER PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Course (
    -- Atributos no relacionales
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,

    -- Atributos relacionales
    tutor_id INTEGER NOT NULL,
    FOREIGN KEY (tutor_id) REFERENCES Tutor(user_id),

    -- Restricciones
    UNIQUE (name, tutor_id) -- Para evitar que el unico elemento identificatorio sea implicito
);

-- Tabla de Unión
CREATE TABLE Student_Course (
    -- Atributos relacionales
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES Student(user_id),
    FOREIGN KEY (course_id) REFERENCES Course(id),
    PRIMARY KEY (student_id, course_id)
);

CREATE TABLE Task (
    -- Atributos no relacionales
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    creation_date TEXT,
    deadline_date TEXT,

    -- Atributos relacionales
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE Criteria (
    -- Atributos no relacionales
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,

    -- Atributos relacionales
    task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES Task(id),

    -- Restricciones 
    UNIQUE (task_id, name) -- En caso de que queramos una única entrega
);

CREATE TABLE Submission (
    -- Atributos no relacionales
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,

    -- Atributos relacionales
    user_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Student(user_id),
    FOREIGN KEY (task_id) REFERENCES Task(id),

    -- Restricciones
    UNIQUE (user_id, task_id)
);

CREATE TABLE Review (
    -- Atributos no relacionales
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    is_pending BOOLEAN NOT NULL DEFAULT 1,
    date TEXT,

    -- Atributos relacionales
    reviewer_id INTEGER NOT NULL,
    submission_id INTEGER NOT NULL,
    FOREIGN KEY (reviewer_id) REFERENCES User(id),
    FOREIGN KEY (submission_id) REFERENCES Submission(id),

    -- Restricciones
    UNIQUE (reviewer_id, submission_id)
);

-- Tabla de unión
CREATE TABLE Review_Criteria (
    -- Atributos no relacionales
    valoracion FLOAT,

    -- Atributos relacionales
    review_id INTEGER NOT NULL,
    criteria_id INTEGER NOT NULL,
    FOREIGN KEY (review_id) REFERENCES Review(id),
    FOREIGN KEY (criteria_id) REFERENCES Criteria(id),
    PRIMARY KEY (review_id, criteria_id)
);
