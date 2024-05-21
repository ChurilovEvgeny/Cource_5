SELECT employers.name, COUNT(*) FROM employers
JOIN vacancies ON employers.id = vacancies.employer_id
GROUP BY employers.id;