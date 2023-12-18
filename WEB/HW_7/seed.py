from faker import Faker
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade, engine

fake = Faker()
Session = sessionmaker(bind=engine)
session = Session()

# Create groups
group_names = ['Group A', 'Group B', 'Group C']
groups = [Group(name=name) for name in group_names]
session.add_all(groups)
session.commit()

# Create teachers
teacher_names = [fake.name() for _ in range(3)]
teachers = [Teacher(name=name) for name in teacher_names]
session.add_all(teachers)
session.commit()

# Create subjects with teacher link
subject_names = ['Math', 'Physics', 'Chemistry', 'Biology', 'History']
subjects = [Subject(name=name, teacher=teachers[i % 3]) for i, name in enumerate(subject_names)]
session.add_all(subjects)
session.commit()

# Create students and grades
students = [Student(name=fake.name(), group=groups[i % len(groups)]) for i in range(30)]
session.add_all(students)
session.commit()

for student in students:
    for subject in subjects:
        grade = Grade(value=fake.random_int(min=1, max=100), date=fake.date_time_this_year(), student=student, subject=subject)
        session.add(grade)
session.commit()
