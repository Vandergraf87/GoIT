SELECT groups.name AS group_name, STRING_AGG(students.fullname, ', ') AS student_list
FROM students
JOIN groups ON students.group_id = groups.id
GROUP BY groups.name;