PRAGMA foreign_keys = ON;

-- Authors
CREATE TABLE IF NOT EXISTS authors (
  id   INTEGER PRIMARY KEY,
  name TEXT    NOT NULL
);

-- Books
CREATE TABLE IF NOT EXISTS books (
  id        INTEGER PRIMARY KEY,
  name      TEXT    NOT NULL,
  author_id INTEGER,
  FOREIGN KEY (author_id) REFERENCES authors(id)
);

-- Customers
CREATE TABLE IF NOT EXISTS customers (
  id    INTEGER PRIMARY KEY,
  name  TEXT    NOT NULL,
  email TEXT    NOT NULL UNIQUE
);

-- Rents
CREATE TABLE IF NOT EXISTS rents (
  id          INTEGER PRIMARY KEY,
  book_id     INTEGER NOT NULL,
  customer_id INTEGER NOT NULL,
  state       TEXT    NOT NULL,
  FOREIGN KEY (book_id)     REFERENCES books(id),
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
