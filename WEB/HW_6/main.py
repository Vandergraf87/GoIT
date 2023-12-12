from utils import (
                    find_student_with_highest_avg_grade_by_subject,
                    find_avg_grade_by_groups,
                    find_top_students_by_avg_grade,
                    find_avg_grade_for_all_grades,
                    find_teachers_vs_subjects,
                    find_students_by_group,
                    find_grades_by_groups_and_subject,
                    find_subjects_for_student,
                    find_avg_grade_by_teacher,
                    find_subjects_for_student_by_teacher)

def main_menu():
    msg = """Please select an option:
    1. Find the 5 students with the highest grade point average across all subjects
    2. Find the student with the highest grade point average for a certain subject
    3. Find the average grade in groups for each subject
    4. Find the average grade on the stream (across the entire scoreboard)
    5. Find which courses are taught by a particular teacher
    6. Find a list of students in a specific group
    7. Find the grades of students in a separate group for a specific subject
    8. Find the average score given by a certain teacher for his subjects
    9. Find a list of courses a student is taking
    10. Find a list of courses taught to a specific student by a specific teacher
    0. Exit
        """
    print(msg)

def process_user_choice(choice):
    if choice == '1':
        top_students = find_top_students_by_avg_grade()
        print("Top 5 sudents with highest GPA:")
        print(top_students)
    elif choice == '2':
        student_highest_avg_grade = find_student_with_highest_avg_grade_by_subject()
        print("Student with the highest GPA for a certain subject:")
        print(student_highest_avg_grade)
    elif choice == '3':
        avg_grade_by_groups = find_avg_grade_by_groups()
        print(f"Average grade in groups for each subjec:")
        print(avg_grade_by_groups)
    elif choice == '4':
        avg_grades_from_grade = find_avg_grade_for_all_grades()
        print(f"Average grade on the stream:")
        print(avg_grades_from_grade)
    elif choice == '5':
        teachers_subjects = find_teachers_vs_subjects()
        print(f"Courses are taught by teachers:")
        print(teachers_subjects)
    elif choice == '6':
        students_by_group = find_students_by_group()
        print(f"Students by groups:")
        print(students_by_group)
    elif choice == '7':
        grades_by_subjects = find_grades_by_groups_and_subject()
        print(f"Student grades by groups and subjects:")
        print(grades_by_subjects)
    elif choice == '8':
        avg_grade_by_subject = find_avg_grade_by_teacher()
        print(f"AVG grades by teacher for his subject:")
        print(avg_grade_by_subject)
    elif choice == '9':
        students_by_subjects = find_subjects_for_student()
        print(f"A list of courses a student is taking:")
        print(students_by_subjects)
    elif choice == '10':
        subjects_for_student_by_teacher = find_subjects_for_student_by_teacher()
        print(f"A list of courses taught to a specific student by a specific teacher:")
        print(subjects_for_student_by_teacher)

if __name__ == '__main__':
    while True:
        main_menu()
        user_choice = input("Enter your selection: ")
        if user_choice == '0':
            print("Thank you for visiting. See you!")
            break
        process_user_choice(user_choice)
