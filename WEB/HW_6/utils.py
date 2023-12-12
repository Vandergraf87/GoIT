from connection import create_connection
from typing import Union

def perform_query_from_file(file_path: str, params: Union[tuple, None] = None):
    with open(file_path, 'r') as file:
        query_str = file.read()

    with create_connection() as conn:
        if conn is not None:
            cur = conn.cursor()
            if params is not None:
                cur.execute(query_str, params)
            else:
                cur.execute(query_str)
            result = cur.fetchall()
            cur.close()
            return result
        else:
            print("Error: can't create the database connection")
            return None

def find_top_students_by_avg_grade():
    """1. Find the 5 students with the highest grade point average across all subjects"""
    query_file_path = "queries/query_1.sql"
    return perform_query_from_file(query_file_path)

def find_student_with_highest_avg_grade_by_subject():
    """2. Find the student with the highest grade point average for a certain subject"""
    query_file_path = "queries/query_2.sql"
    return perform_query_from_file(query_file_path)

def find_avg_grade_by_groups():
    """3. Find the average grade in groups for each subject"""
    query_file_path = "queries/query_3.sql"
    return perform_query_from_file(query_file_path)

def find_avg_grade_for_all_grades():
    """4. Find the average grade on the stream (across the entire scoreboard)"""
    query_file_path = "queries/query_4.sql"
    return perform_query_from_file(query_file_path)

def find_teachers_vs_subjects():
    """5. Find which courses are taught by a particular teacher"""
    query_file_path = "queries/query_5.sql"
    return perform_query_from_file(query_file_path)

def find_students_by_group():
    """6. Find a list of students in a specific group"""
    query_file_path = "queries/query_6.sql"
    return perform_query_from_file(query_file_path)

def find_grades_by_groups_and_subject():
    """7. Find the grades of students in a separate group for a specific subject"""
    query_file_path = "queries/query_7.sql"
    return perform_query_from_file(query_file_path)

def find_avg_grade_by_teacher():
    """8. Find the average score given by a certain teacher for his subjects"""
    query_file_path = "queries/query_8.sql"
    return perform_query_from_file(query_file_path)

def find_subjects_for_student():
    """9. Find a list of courses a student is taking"""
    query_file_path = "queries/query_9.sql"
    return perform_query_from_file(query_file_path)

def find_subjects_for_student_by_teacher():
    """10. Find a list of courses taught to a specific student by a specific teacher"""
    query_file_path = "queries/query_10.sql"
    return perform_query_from_file(query_file_path)