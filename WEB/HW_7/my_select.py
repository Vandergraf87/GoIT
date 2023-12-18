from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import select, func, desc, alias
from models import Student, Grade, Group, Subject, Teacher, engine

Session = sessionmaker(bind=engine)
session = Session()

# Query 1
def select_1():
    query = session.query(Student.id, Student.name, func.avg(Grade.value).label('avg_grade')) \
    .join(Grade, Student.id == Grade.student_id) \
    .group_by(Student.id) \
    .order_by(desc('avg_grade')) \
    .limit(5) \
    .all()
    return query

# Query 2
def select_2():
    subject_id = 1  # Change for another subject
    query = session.query(Student.id, Student.name, func.avg(Grade.value).label('avg_grade')) \
    .join(Grade, Student.id == Grade.student_id) \
    .filter(Grade.subject_id == subject_id) \
    .group_by(Student.id) \
    .order_by(desc('avg_grade')) \
    .limit(1) \
    .first()
    return query

# Query 3
def select_3():
    subject_name = 'Math' # Change for another subject

    subject = session.query(Subject).filter_by(name=subject_name).first()

    if subject:
        result = (
    session.query(Group.name, func.avg(Grade.value).label('average_grade'))
    .join(Student, Group.students)
    .join(Grade, Student.grades)
    .join(Subject, Grade.subject)  
    .filter(Subject.name == subject.name)  
    .group_by(Group.name)
    .all()
)
    return result

# Query 4
def select_4():
    result = session.query(func.avg(Grade.value).label('average_grade')).scalar()
    return result

# Query 5
def select_5():
    teacher_id = 1  # Change for another teacher
    result = (
    session.query(Subject.name)
    .filter(Subject.teacher_id == teacher_id)
    .distinct()
    .all()
)
    return result

# Query 6
def select_6():
    group_id = 1  # Change for another group
    result = (
    session.query(Student.name)
    .filter(Student.group_id == group_id)
    .all()
)
    return result

# Query 7
def select_7():
    group_id = 1  # Change for another group
    subject_id = 1  # Change for another subject
    result = (
    session.query(Student.name, Grade.value)
    .join(Grade, Student.grades)
    .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
    .all()
)
    return result

# Query 8
def select_8():
    teacher_id = 1  # Change for another teacher
    result = (
    session.query(func.avg(Grade.value).label('average_grade'))
    .join(Subject, Grade.subject)
    .filter(Subject.teacher_id == teacher_id)
    .scalar()
)
    return result

# Query 9
def select_9():
    student_id = 1  # Change for another student
    result = (
    session.query(Subject.name)
    .join(Grade, Subject.grades)
    .filter(Grade.student_id == student_id)
    .distinct()
    .all()
)
    return result

# Query 10
def select_10():
    student_id = 1  # Change for another student
    teacher_id = 1  # Change for another teacher
    result = (
    session.query(Subject.name)
    .join(Grade, Subject.grades)
    .join(Student, Grade.student)
    .filter(Student.id == student_id, Subject.teacher_id == teacher_id)
    .distinct()
    .all()
)
    return result


print("Result 1:", select_1())
print("Result 2:", select_2())
print("Result 3:", select_3())
print("Result 4:", select_4())
print("Result 5:", select_5())
print("Result 6:", select_6())
print("Result 7:", select_7())
print("Result 8:", select_8())
print("Result 9:", select_9())
print("Result 10:", select_10())