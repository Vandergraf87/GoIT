from psycopg2 import DatabaseError
from connection import create_connection


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except DatabaseError as err:
        print(err)


if __name__ == '__main__':
    table_groups = """CREATE TABLE IF NOT EXISTS groups (
     id SERIAL PRIMARY KEY,
     name VARCHAR(50) NOT NULL
    );"""
    table_students = """CREATE TABLE IF NOT EXISTS students (
     id SERIAL PRIMARY KEY,
     fullname VARCHAR(150) NOT NULL,
     group_id INTEGER REFERENCES groups(id)
         on delete cascade
    );"""
    table_teachers = """CREATE TABLE IF NOT EXISTS teachers (
      id SERIAL PRIMARY KEY,
      fullname VARCHAR(150) NOT NULL
    );"""
    table_subjects = """CREATE TABLE IF NOT EXISTS subjects (
      id SERIAL PRIMARY KEY,
      name VARCHAR(175) NOT NULL,
      teacher_id INTEGER  REFERENCES teachers(id)
        on delete cascade
    );"""
    table_grades = """CREATE TABLE IF NOT EXISTS grades (
      id SERIAL PRIMARY KEY,
      student_id INTEGER  REFERENCES students(id)
      on delete cascade,
      subject_id INTEGER  REFERENCES subjects(id)
      on delete cascade,
      grade INTEGER CHECK (grade >= 0 AND grade <= 100),
      grade_date DATE NOT NULL
    );"""

    with create_connection() as conn:
        if conn is not None:
            create_table(conn, table_groups)
            create_table(conn, table_students)
            create_table(conn, table_teachers)
            create_table(conn, table_subjects)
            create_table(conn, table_grades)
            conn.commit()
        else:
            print("Error: can't create the database connection")
