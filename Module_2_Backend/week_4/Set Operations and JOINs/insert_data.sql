
-- Insert data into authors
INSERT INTO authors (id, name) VALUES
  (1, 'Miguel de Cervantes'),
  (2, 'Dante Alighieri'),
  (3, 'Takehiko Inoue'),
  (4, 'Akira Toriyama'),
  (5, 'Walt Disney');

-- Insert data into books
INSERT INTO books (id, name, author_id) VALUES
  (1, 'Don Quijote',            1),
  (2, 'La Divina Comedia',      2),
  (3, 'Vagabond 1-3',           3),
  (4, 'Dragon Ball 1',          4),
  (5, 'The Book of the 5 Rings', NULL);

-- Insert data into customers
INSERT INTO customers (id, name, email) VALUES
  (1, 'John Doe',        'j.doe@email.com'),
  (2, 'Jane Doe',        'jane@doe.com'),
  (3, 'Luke Skywalker',  'darth.son@email.com');

-- Insert data into rents
INSERT INTO rents (id, book_id, customer_id, state) VALUES
  (1, 1, 2, 'Returned'),
  (2, 2, 2, 'Returned'),
  (3, 1, 1, 'On time'),
  (4, 3, 1, 'On time'),
  (5, 2, 2, 'Overdue');
