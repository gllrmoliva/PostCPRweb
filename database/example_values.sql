-- Este script tiene la función de rellenar la base de datos (idealmente vacia) con valores de ejemplo

-- Usuarios de ejemplo
INSERT INTO User
(email, password, name) VALUES
("john@mail.com", "1234", "John"),
("alice@mail.com", "5678", "Alice"),
("james@mail.com", "dogs", "James"),
("mary@mail.com", "cats", "Mary"),
("matt@mail.com", "hello", "Matthew"),
("kim@mail.com", "hello", "Kimberly");

-- Estudiantes de ejemplo
INSERT INTO Student
(user_id)
SELECT id FROM User WHERE 
email = "john@mail.com" OR
email = "alice@mail.com" OR
email = "james@mail.com" OR
email = "mary@mail.com";

-- Profesores de ejemplo
INSERT INTO Tutor
(user_id)
SELECT id FROM User WHERE
email = "matt@mail.com" OR
email = "kim@mail.com";

-- Cursos de ejemplo
INSERT INTO Course (name, tutor_id)
SELECT "Calculus I", id FROM User WHERE email = "matt@mail.com";
INSERT INTO Course (name, tutor_id)
SELECT "Calculus II", id FROM User WHERE email = "matt@mail.com";
INSERT INTO Course (name, tutor_id)
SELECT "Algebra I", id FROM User WHERE email = "kim@mail.com";
INSERT INTO Course (name, tutor_id)
SELECT "Algebra II", id FROM User WHERE email = "kim@mail.com";

-- Uniones Estudiante_Curso de ejemplo
INSERT INTO Student_Course (student_id, course_id)
SELECT
    User.id,
    Course.id
FROM
    (SELECT id FROM User WHERE email IN ("john@mail.com", "alice@mail.com")) AS User
CROSS JOIN
    (SELECT id FROM Course WHERE name IN ("Calculus I", "Algebra I")) AS Course;

INSERT INTO Student_Course (student_id, course_id)
SELECT
    User.id,
    Course.id
FROM
    (SELECT id FROM User WHERE email IN ("james@mail.com", "mary@mail.com")) AS User
CROSS JOIN
    (SELECT id FROM Course WHERE name IN ("Calculus II", "Algebra II")) AS Course;

-- Tareas de ejemplo
-- Tareas de ejemplo con descripciones
INSERT INTO Task (name, course_id, instructions, creation_date, deadline_date)
SELECT "Task 1: Limits", id, "Explore and understand the concept of limits in calculus.", '2024-04-28', '2024-05-15' FROM Course WHERE name = "Calculus I";

INSERT INTO Task (name, course_id, instructions, creation_date, deadline_date)
SELECT "Task 2: Derivatives", id, "Study the fundamental principles of derivatives and their applications.", '2024-04-28', '2024-05-15' FROM Course WHERE name = "Calculus I";

INSERT INTO Task (name, course_id, instructions, creation_date, deadline_date)
SELECT "Task 1: Integrals", id, "Introduction to integral calculus, focusing on basic integration techniques.", '2024-04-28', '2024-05-22' FROM Course WHERE name = "Calculus II";

INSERT INTO Task (name, course_id, instructions, creation_date, deadline_date)
SELECT "Task 1: Functions", id, "Examine different types of functions and their properties.", '2024-04-28', '2024-05-10' FROM Course WHERE name = "Algebra I";

INSERT INTO Task (name, course_id, instructions, creation_date, deadline_date)
SELECT "Task 2: Trigonometry", id, "Explore trigonometric functions and their uses in solving problems.", '2024-04-28', '2024-05-10' FROM Course WHERE name = "Algebra I";

INSERT INTO Task (name, course_id, instructions, creation_date, deadline_date)
SELECT "Task 1: Vectors", id, "Learn about vectors, their operations, and applications in various fields.", '2024-04-28', '2024-05-18' FROM Course WHERE name = "Algebra II";




-- Criterios de ejemplo
INSERT INTO Criterion (name, task_id)
SELECT "Puntualidad", id FROM Task;
INSERT INTO Criterion (name, task_id)
SELECT "Ortografía", id FROM Task WHERE name = "Task 1: Integrals";
INSERT INTO Criterion (name, task_id)
SELECT "Ortografía", id FROM Task WHERE name = "Task 1: Vectors";