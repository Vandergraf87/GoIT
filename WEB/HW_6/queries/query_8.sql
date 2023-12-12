SELECT teachers.fullname, ROUND(AVG(grades.grade), 2) as average_grade
FROM teachers
JOIN subjects ON teachers.id = subjects.teacher_id
JOIN grades ON subjects.id = grades.subject_id
GROUP BY teachers.fullname;