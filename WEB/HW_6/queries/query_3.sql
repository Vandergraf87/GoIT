SELECT subjects.name AS subject_name, groups.name AS group_name, ROUND(AVG(grades.grade), 2) AS average_grade
FROM subjects
CROSS JOIN groups
LEFT JOIN students ON groups.id = students.group_id
LEFT JOIN grades ON students.id = grades.student_id AND subjects.id = grades.subject_id
GROUP BY subjects.id, groups.id
ORDER BY subject_name, group_name;