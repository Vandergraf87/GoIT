SELECT
  subjects.name AS subject_name,
  students.fullname AS student_name,
  ROUND(AVG(grades.grade), 2) AS average_grade
FROM subjects
JOIN grades ON subjects.id = grades.subject_id
JOIN students ON grades.student_id = students.id
GROUP BY subjects.id, students.id
ORDER BY subjects.name, average_grade DESC;