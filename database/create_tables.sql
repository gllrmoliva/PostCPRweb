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
    instructions TEXT,
    creation_date TEXT,
    deadline_date TEXT,

    -- Atributos relacionales
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Course(id)

    -- Restricciones
    UNIQUE (name, course_id) -- Para evitar que el unico elemento identificatorio sea implicito
);

CREATE TABLE Criterion (
    -- Atributos no relacionales
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,

    -- Atributos relacionales
    task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES Task(id),

    -- Restricciones 
    UNIQUE (name, task_id) -- Para evitar que el unico elemento identificatorio sea implicito
);

CREATE TABLE Submission (
    -- Atributos no relacionales
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,

    -- Atributos relacionales
    student_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Student(user_id),
    FOREIGN KEY (task_id) REFERENCES Task(id),

    -- Restricciones
    UNIQUE (student_id, task_id) -- En caso de que queramos una única entrega
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
    UNIQUE (reviewer_id, submission_id) -- En caso de que queramos que una misma persona no puede revisar la misma entrega dos veces
);

-- Tabla de unión
CREATE TABLE Review_Criterion (
    -- Atributos no relacionales
    valoracion FLOAT,

    -- Atributos relacionales
    review_id INTEGER NOT NULL,
    criterion_id INTEGER NOT NULL,
    FOREIGN KEY (review_id) REFERENCES Review(id),
    FOREIGN KEY (criterion_id) REFERENCES Criterion(id),
    PRIMARY KEY (review_id, criterion_id)
);
