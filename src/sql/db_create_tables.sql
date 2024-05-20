CREATE TABLE IF NOT EXISTS employers
(
	id INT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	alternate_url VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS vacancies
(
	id INT PRIMARY KEY,
	employer_id INT,
	name VARCHAR(255) NOT NULL,
	alternate_url VARCHAR(255) NOT NULL,
	area_name VARCHAR(255) NOT NULL,
	schedule VARCHAR(50) NOT NULL DEFAULT('Не указано'),

	FOREIGN KEY (employer_id) REFERENCES employers(id)
);

CREATE TABLE IF NOT EXISTS salaries
(
	vacancy_id INT PRIMARY KEY REFERENCES vacancies(id),
	sal_from INT,
    sal_to INT,
    currency VARCHAR(10),
    gross BOOLEAN NOT NULL DEFAULT(FALSE)
);

-- Дополнительное ограничение для формирования отношения 1 к 1
ALTER TABLE vacancies
ADD CONSTRAINT fk_vacancies_id
FOREIGN KEY (id) REFERENCES salaries (vacancy_id) DEFERRABLE INITIALLY DEFERRED;