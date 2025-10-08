WITH departament_hires AS (
    SELECT
        d.id,
        d.name AS department_name,
        COUNT(e.id) AS hires
    FROM
        employees e
    JOIN
        departments d ON e.department_id = d.id
    WHERE
        EXTRACT(YEAR FROM e.hire_date) = 2021
    GROUP BY
        d.id
), average_hires AS (
    SELECT
        AVG(hires) AS average_hires
    FROM
        departament_hires
)
SELECT
    dh.id,
    dh.department_name,
    dh.hires AS department_hired
FROM
    departament_hires dh
JOIN
    average_hires ah
WHERE
    dh.hires > ah.average_hires
ORDER BY
    dh.hires DESC;
