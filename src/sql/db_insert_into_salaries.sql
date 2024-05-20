INSERT INTO salaries
VALUES(%, %, %, %, %)
ON CONFLICT(vacancy_id) DO UPDATE
SET
sal_from = EXCLUDED.sal_from,
sal_to = EXCLUDED.sal_to,
currency = EXCLUDED.currency,
gross = EXCLUDED.gross;