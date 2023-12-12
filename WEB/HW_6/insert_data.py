from datetime import datetime

from faker import Faker
from random import randint, sample
from connection import create_connection

fake = Faker('uk-Ua')

def reset_sequence(table_name, column_name):
    with create_connection() as conn:
        if conn is not None:
            cur = conn.cursor()
            cur.execute(f"ALTER SEQUENCE {table_name}_{column_name}_seq RESTART WITH 1;")
            conn.commit()
            cur.close()
        else:
            print('Error: can\'t create the database connection')

def generate_fake_group_name():
    department = fake.random_element(elements=('ПБ', 'ПК', 'ПГ'))
    group_number = fake.random_int(min=10, max=99)

    return f"{department}-{group_number}"


def generate_fake_subject_name():
    return fake.random_element(
        elements=('Вища математика', 'Фізика', 'Хімія',
                  'Програмування', 'Українська мова', 'Література',
                  'Автоматизація', 'Електротехніка'))

def generate_fake_date(start_date='2023-09-01', end_date=datetime.now().strftime('%Y-%m-%d')):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    fake_datetime = fake.date_time_between(start_date=start_datetime, end_date=end_datetime)
    return fake_datetime


if __name__ == '__main__':
    sql_insert_groups_table = "INSERT INTO groups(name) VALUES(%s)"
    sql_insert_students_table = "INSERT INTO students(fullname, group_id) VALUES(%s, %s)"
    sql_insert_teachers_table = "INSERT INTO teachers(fullname) VALUES(%s)"
    sql_insert_subjects_table = "INSERT INTO subjects(name, teacher_id) VALUES(%s, %s)"
    sql_insert_grades_table = "INSERT INTO grades(student_id, subject_id, grade, grade_date) VALUES(%s, %s, %s, %s)"

    with create_connection() as conn:
        if conn is not None:
            cur = conn.cursor()
            reset_sequence('groups', 'id')
            reset_sequence('students', 'id')
            reset_sequence('teachers', 'id')
            reset_sequence('subjects', 'id')
            reset_sequence('grades', 'id')

            # add groups
            for _ in range(3):
                cur.execute(sql_insert_groups_table, (generate_fake_group_name(),))

            # add students
            cur.execute("SELECT id FROM groups")
            group_ids = [row[0] for row in cur.fetchall()]
            for _ in range(50):
                cur.execute(sql_insert_students_table, (fake.name(), fake.random_element(elements=group_ids)))

            # add teachers
            for _ in range(5):
                cur.execute(sql_insert_teachers_table, (fake.name(),))

            # add subjects
            cur.execute("SELECT id FROM teachers")
            teachers_ids = [row[0] for row in cur.fetchall()]
            subjects_per_teacher = {teacher_id: 1 for teacher_id in teachers_ids}
            remaining_subjects = 8 - len(teachers_ids)

            while remaining_subjects > 0:
                for teacher_id in teachers_ids:
                    if remaining_subjects > 0 and fake.boolean(chance_of_getting_true=50):
                        subjects_per_teacher[teacher_id] += 1
                        remaining_subjects -= 1
            subject_names = set()
            for teacher_id, num_subjects in subjects_per_teacher.items():
                for _ in range(num_subjects):
                    subject_name = generate_fake_subject_name()
                    while subject_name in subject_names:
                        subject_name = generate_fake_subject_name()
                    subject_names.add(subject_name)

                    cur.execute(sql_insert_subjects_table, (subject_name, teacher_id))

            #add grades
            cur.execute("SELECT id FROM subjects")
            subject_ids = [row[0] for row in cur.fetchall()]
            cur.execute("SELECT id FROM students")
            student_ids = [row[0] for row in cur.fetchall()]
            for student_id in student_ids:
                num_grades = min(randint(12, 20), len(subject_ids))
                selected_subjects = sample(subject_ids, num_grades)
                for subject_id in selected_subjects:
                    num_grades_per_subject = randint(1, 5)
                    for _ in range(num_grades_per_subject):
                        cur.execute(sql_insert_grades_table,
                                    (student_id, subject_id, randint(0, 100), generate_fake_date()))
            conn.commit()
            cur.close()
        else:
            print('Error: can\'t create the database connection')
