PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS customers (
  customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name    TEXT    NOT NULL,
  last_name     TEXT,
  phone_number  TEXT    NOT NULL,
  address       TEXT    NOT NULL
);


CREATE TABLE IF NOT EXISTS items (
  item_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name      TEXT    NOT NULL,
  price     REAL    NOT NULL 
);


CREATE TABLE IF NOT EXISTS orders (
  order_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id   INTEGER NOT NULL,
  delivery_time DATETIME NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


CREATE TABLE IF NOT EXISTS order_items (
  order_id        INTEGER NOT NULL,
  item_id         INTEGER NOT NULL,
  quantity        INTEGER NOT NULL,
  special_request TEXT,
  PRIMARY KEY (order_id, item_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (item_id)  REFERENCES items(item_id)
);


-- ADD THE DATA FROM THE PREVIOUS TABLE 

PRAGMA foreign_keys = ON;

--Customers
INSERT INTO customers (first_name, last_name, phone_number, address) VALUES
  ('Alice', NULL, '123-456-7890', '123 Main St'),        -- customer_id = 1
  ('Bob',   NULL, '987-654-3210', '456 Elm St'),         -- customer_id = 2
  ('Claire',NULL, '555-123-4567', '789 Oak St'),         -- customer_id = 3
  ('Claire',NULL, '555-123-4567', '464 Georgia St');     -- customer_id = 4


--Items
INSERT INTO items (item_id, name, price) VALUES
  (101, 'Cheeseburger',  8.00),
  (102, 'Fries',         3.00),
  (103, 'Pizza',        12.00),
  (104, 'Fries',         2.00),
  (105, 'Salad',         6.00),
  (106, 'Water',         1.00);


--Orders
INSERT INTO orders (order_id, customer_id, delivery_time) VALUES
  (1, 1, '18:00:00'),   -- Order 001 de Alice
  (2, 2, '19:30:00'),   -- Order 002 de Bob
  (3, 3, '12:00:00'),   -- Order 003 de Claire (789 Oak St)
  (4, 4, '17:00:00');   -- Order 004 de Claire (464 Georgia St)


--Order_Items
INSERT INTO order_items (order_id, item_id, quantity, special_request) VALUES
  (1, 101, 2, 'No onions'),
  (1, 102, 1, 'Extra ketchup'),
  (2, 103, 1, 'Extra cheese'),
  (2, 104, 2, 'None'),
  (3, 105, 1, 'No croutons'),
  (4, 106, 1, 'None');


-- TESTING 

SELECT
  o.order_id,
  c.first_name 
    || COALESCE(' ' || c.last_name, '') 
    AS customer_name,
  c.phone_number,
  c.address,
  oi.item_id,
  i.name       AS item_name,
  i.price,
  oi.quantity,
  COALESCE(oi.special_request, 'None') AS special_request,
  o.delivery_time
FROM orders         AS o
JOIN customers     AS c  ON o.customer_id = c.customer_id
JOIN order_items   AS oi ON o.order_id    = oi.order_id
JOIN items         AS i  ON oi.item_id    = i.item_id
ORDER BY o.order_id, oi.item_id;
