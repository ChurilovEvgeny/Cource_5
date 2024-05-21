SELECT vacancies.name, employers.name, salaries.sal_from, salaries.sal_to, salaries.currency from vacancies
JOIN employers ON employers.id = vacancies.employer_id
JOIN salaries ON salaries.vacancy_id = vacancies.id
WHERE ABS(COALESCE(salaries.sal_to, 0) - COALESCE(salaries.sal_from, 0)) > (
	SELECT
	AVG(ABS(COALESCE(salaries.sal_to, 0) - COALESCE(salaries.sal_from, 0)))
	FROM vacancies
	JOIN salaries ON salaries.vacancy_id = vacancies.id
);
