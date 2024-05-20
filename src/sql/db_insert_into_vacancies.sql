INSERT INTO vacancies
VALUES(%, %, %, %, %)
ON CONFLICT(id) DO UPDATE
SET
employer_id = EXCLUDED.employer_id,
name = EXCLUDED.name,
alternate_url = EXCLUDED.alternate_url,
area_name = EXCLUDED.area_name;