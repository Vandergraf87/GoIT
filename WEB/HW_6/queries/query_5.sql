SELECT
    teachers.fullname AS teacher_name,
    ARRAY_AGG(subjects.name) AS taught_subjects
FROM
    teachers
JOIN subjects ON teachers.id = subjects.teacher_id
GROUP BY
    teachers.id;