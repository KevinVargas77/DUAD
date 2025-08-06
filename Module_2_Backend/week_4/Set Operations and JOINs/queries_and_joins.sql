SELECT
  b.id            AS book_id,
  b.name          AS book_name,
  COALESCE(a.name, 'Unknown') AS author_name
FROM books AS b
LEFT JOIN authors AS a
  ON b.author_id = a.id;


SELECT
  id      AS book_id,
  name    AS book_name
FROM books
WHERE author_id IS NULL;


SELECT
  a.id   AS author_id,
  a.name AS author_name
FROM authors AS a
LEFT JOIN books AS b
  ON b.author_id = a.id
WHERE b.id IS NULL;


SELECT DISTINCT
  b.id       AS book_id,
  b.name     AS book_name
FROM books AS b
INNER JOIN rents AS r
  ON b.id = r.book_id;


SELECT DISTINCT
  b.id       AS book_id,
  b.name     AS book_name
FROM books AS b
LEFT JOIN rents AS r
  ON b.id = r.book_id
WHERE  r.book_id IS NULL


SELECT DISTINCT
  c.id       AS customer_id,
  c.name     AS customer_name
FROM customers AS c
LEFT JOIN rents AS r
  ON c.id = r.customer_id
WHERE  r.book_id IS NULL


SELECT DISTINCT
  b.id      AS book_id,
  b.name    AS book_name
FROM books AS b
INNER JOIN rents AS r
  ON b.id = r.book_id
WHERE r.state = 'Overdue';
