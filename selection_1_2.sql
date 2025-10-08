SELECT 
    d.name AS department_name,
    j.title AS job_title,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM e.hire_date) = 1 THEN e.id END) AS Q1,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM e.hire_date) = 2 THEN e.id END) AS Q2,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM e.hire_date) = 3 THEN e.id END) AS Q3,
    COUNT(CASE WHEN EXTRACT(QUARTER FROM e.hire_date) = 4 THEN e.id END) AS Q4
FROM
    employees e
JOIN
    departments d ON e.department_id = d.id
JOIN
    jobs j ON e.job_id = j.id
WHERE
    EXTRACT(YEAR FROM e.hire_date) = 2021
GROUP BY
    d.name, j.title
ORDER BY
    department_name ASC, job_title ASC;