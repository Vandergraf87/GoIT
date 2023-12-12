SELECT students.fullname AS student_name,
       ARRAY_AGG(DISTINCT subjects.name) AS subjects_list
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
GROUP BY students.id;