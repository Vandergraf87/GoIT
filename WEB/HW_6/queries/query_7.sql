SELECT subjects.name AS subject_name, groups.name AS group_name,
                ARRAY_AGG(DISTINCT students.fullname) AS student_list
FROM students
JOIN grades ON students.id = grades.student_id
JOIN groups ON students.group_id = groups.id
JOIN subjects ON grades.subject_id = subjects.id
GROUP BY subjects.name, groups.name;