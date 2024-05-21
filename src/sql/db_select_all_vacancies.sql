SELECT vacancies.name, employers.name, salaries.sal_from, salaries.sal_to, salaries.currency FROM vacancies
JOIN employers ON employers.id = vacancies.employer_id
JOIN salaries ON salaries.vacancy_id = vacancies.id;
