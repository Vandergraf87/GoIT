SELECT students.fullname AS student_name,
       ARRAY_AGG(DISTINCT subjects.name || ' - ' || teachers.fullname) AS subjects_and_teachers
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
JOIN teachers ON subjects.teacher_id = teachers.id
GROUP BY students.id;