-- Проверка на существование таблиц (1 - все есть, 0 - если нет хотя бы одной)
SELECT CAST(COUNT(*) AS BIT) -- Should be unique to give 0 or 1 as result
FROM INFORMATION_SCHEMA.TABLES
WHERE table_name = 'employers' OR table_name = 'salaries' OR table_name = 'vacancies';