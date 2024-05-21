SELECT
AVG(ABS(COALESCE(salaries.sal_to, 0) - COALESCE(salaries.sal_from, 0)))
FROM vacancies
JOIN salaries ON salaries.vacancy_id = vacancies.id;
