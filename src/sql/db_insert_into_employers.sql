INSERT INTO employers
VALUES(%s, %s, %s)
ON CONFLICT(id) DO UPDATE
SET name = EXCLUDED.name, alternate_url = EXCLUDED.alternate_url;
