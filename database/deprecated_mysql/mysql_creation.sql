/* Creación de la base de datos */

DROP DATABASE IF EXISTS test;
CREATE DATABASE test;
USE test;

/* Creación de tablas */

CREATE TABLE User (
    /* Atributos no relacionales */
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL

    /* Atributos relacionales */

);

CREATE TABLE Tutor (
    /* Atributos no relacionales */

    /* Atributos relacionales */
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Student (
    /* Atributos no relacionales */
    
    /* Atributos relacionales */
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Course (
    /* Atributos no relacionales */
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,

    /* Atributos relacionales */
    tutor_id INT NOT NULL,
    FOREIGN KEY (tutor_id) REFERENCES Tutor(user_id),

    /* Restricciones */
    UNIQUE (name, tutor_id) /* Para evitar que el unico elemento identificatorio sea implicito */
);

/* Tabla de Unión */
CREATE TABLE Student_Course (
    /* Atributos no relacionales */

    /* Atributos relacionales */
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES Student(user_id),
    FOREIGN key (course_id) REFERENCES Course(id),
    PRIMARY KEY (student_id, course_id)
);

CREATE TABLE Task (
    /* Atributos no relacionales */
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    creation_date date,
    deadline_date date,

    /* Atributos relacionales */
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE Criteria (
    /* Atributos no relacionales */
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,

    /* Atributos relacionales */
    task_id INT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES Task(id),

    /* Restricciones */
    UNIQUE (task_id, name)
);

CREATE TABLE Submission (
    /* Atributos no relacionales */
    id INT AUTO_INCREMENT PRIMARY KEY,
    date date,

    /* Atributos relacionales */
    user_id INT NOT NULL,
    task_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Student(user_id),
    FOREIGN KEY (task_id) REFERENCES Task(id),

    /* Restricciones */
    UNIQUE (user_id, task_id) /* En caso de que queramos una única entrega */
);

CREATE TABLE Review (
    /* Atributos no relacionales */
    id INT AUTO_INCREMENT PRIMARY KEY,
    is_pending BOOLEAN NOT NULL DEFAULT 1,
    date date,

    /* Atributos relacionales */
    reviewer_id INT NOT NULL,
    submission_id INT NOT NULL,
    FOREIGN KEY (reviewer_id) REFERENCES User(id),
    FOREIGN KEY (submission_id) REFERENCES Submission(id),

    /* Restricciones */
    UNIQUE (reviewer_id, submission_id)
);

/* Tabla de Unión */
CREATE TABLE Review_Criteria (
    /* Atributos no relacionales */
    valoracion FLOAT(3,2), /* Rango: .9,99 a 9.99 */

    /* Atributos relacionales */
    review_id INT NOT NULL,
    criteria_id INT NOT NULL,
    FOREIGN KEY (review_id) REFERENCES Review(id),
    FOREIGN KEY (criteria_id) REFERENCES Criteria(id),
    PRIMARY KEY (review_id, criteria_id)
);