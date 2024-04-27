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