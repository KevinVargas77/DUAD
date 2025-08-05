PRAGMA foreign_keys = ON;

--Users
CREATE TABLE IF NOT EXISTS users (
  user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name  TEXT    NOT NULL,
  last_name   TEXT,
  email       TEXT    NOT NULL UNIQUE,
  phone       TEXT
);

--Products
CREATE TABLE IF NOT EXISTS products (
  product_code    TEXT    PRIMARY KEY,
  name            TEXT    NOT NULL,
  price           REAL    NOT NULL CHECK(price >= 0),
  entry_date      DATE,
  brand           TEXT
);

--Shopping Carts (each cart belongs to one user)
CREATE TABLE IF NOT EXISTS shopping_carts (
  cart_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id     INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);

--Invoices (each cart can generate at most one invoice, and each invoice has a buyer)
CREATE TABLE IF NOT EXISTS invoices (
  invoice_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  cart_id           INTEGER NOT NULL UNIQUE,
  buyer_user_id     INTEGER NOT NULL,
  purchase_date     DATETIME DEFAULT (datetime('now','localtime')),
  total_amount      REAL    NOT NULL CHECK(total_amount >= 0),
  FOREIGN KEY (cart_id)        REFERENCES shopping_carts (cart_id),
  FOREIGN KEY (buyer_user_id)  REFERENCES users          (user_id)
);

--Cart.Products (many-to-many between shopping_carts and products)
CREATE TABLE IF NOT EXISTS cart_products (
  cart_id         INTEGER NOT NULL,
  product_code    TEXT    NOT NULL,
  quantity        INTEGER NOT NULL CHECK(quantity > 0),
  PRIMARY KEY (cart_id, product_code),
  FOREIGN KEY (cart_id)       REFERENCES shopping_carts (cart_id),
  FOREIGN KEY (product_code)  REFERENCES products       (product_code)
);

-- Invoice.Products (many-to-many between invoices and products)
CREATE TABLE IF NOT EXISTS invoice_products (
  product_code    TEXT    NOT NULL,
  invoice_id      INTEGER NOT NULL,
  quantity        INTEGER NOT NULL CHECK(quantity > 0),
  PRIMARY KEY (product_code, invoice_id),
  FOREIGN KEY (product_code) REFERENCES products (product_code),
  FOREIGN KEY (invoice_id)   REFERENCES invoices (invoice_id)
);
