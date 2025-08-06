PRAGMA foreign_keys = ON;

--Users
INSERT INTO users (first_name, last_name, email, phone) VALUES
  ('María',   'González',  'maria.gonzalez@gmail.com',  '+506 7123-4567'),
  ('Juan',    'Pérez',     'juan.perez@gmail.com',      '+506 7222-3344'),
  ('Laura',   'Martínez',  'laura.martinez@gmail.com', '+506 7333-2211'),
  ('Carlos',  'Rodríguez', 'carlos.rodriguez@gmail.com','+506 7444-3322'),
  ('Sofía',   'Hernández','sofia.hernandez@gmail.com', '+506 7555-4433'),
  ('Diego',   'López',    'diego.lopez@gmail.com',     '+506 7666-5544'),
  ('Valeria', 'Castro',   'valeria.castro@gmail.com',  '+506 7777-6655'),
  ('Andrés',  'Fernández','andres.fernandez@gmail.com','+506 7888-7766'),
  ('Natalia', 'Gómez',    'natalia.gomez@gmail.com',   '+506 7999-8877'),
  ('José',    'Sánchez',  'jose.sanchez@gmail.com',    '+506 7000-9988');

--Products
INSERT INTO products (product_code, name, price, entry_date, brand) VALUES
  ('P001','Wireless Mouse',           29.99,'2025-06-10','Logitech'),
  ('P002','Mechanical Keyboard',      89.50,'2025-06-12','Corsair'),
  ('P003','27-inch Monitor',         199.99,'2025-06-15','Dell'),
  ('P004','USB-C Hub 7-in-1',         49.95,'2025-06-18','Anker'),
  ('P005','External SSD 1TB',        129.00,'2025-06-20','Samsung'),
  ('P006','Webcam 1080p',             59.99,'2025-06-22','Logitech'),
  ('P007','Noise-Cancelling Headset',119.99,'2025-06-25','Sony'),
  ('P008','Smartphone Stand',         19.99,'2025-06-27','Nulaxy'),
  ('P009','Laptop Sleeve 15″',        25.00,'2025-06-29','Case Logic'),
  ('P010','Portable Charger 20,000mAh',39.95,'2025-07-01','Anker');

--Shopping Carts
INSERT INTO shopping_carts (user_id) VALUES
  (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);

--Cart.Products
INSERT INTO cart_products (cart_id, product_code, quantity) VALUES
  (1,'P001',2),(1,'P004',1),
  (2,'P003',1),(2,'P006',2),(2,'P009',1),
  (3,'P002',1),
  (4,'P005',3),
  (5,'P007',1),(5,'P010',2),
  (6,'P001',1),(6,'P008',1),
  (7,'P003',2),(7,'P006',1),
  (8,'P002',2),
  (9,'P009',1),(9,'P010',1),
  (10,'P005',1);

--Invoices
INSERT INTO invoices
  (cart_id, buyer_user_id, purchase_date, total_amount, buyer_phone, employee_code)
VALUES
  (1,1,'2025-07-02 10:15:00',109.93,'+506 7123-4567','EMP001'),
  (2,2,'2025-07-03 14:30:00',344.97,'+506 7222-3344','EMP002'),
  (3,3,'2025-07-04 09:45:00', 89.50,'+506 7333-2211','EMP003'),
  (4,4,'2025-07-05 16:20:00',387.00,'+506 7444-3322','EMP004'),
  (5,5,'2025-07-06 11:05:00',199.89,'+506 7555-4433','EMP005'),
  (6,6,'2025-07-07 13:40:00', 49.98,'+506 7666-5544','EMP006'),
  (7,7,'2025-07-08 17:10:00',459.97,'+506 7777-6655','EMP007'),
  (8,8,'2025-07-09 08:25:00',179.00,'+506 7888-7766','EMP008'),
  (9,9,'2025-07-10 12:55:00', 64.95,'+506 7999-8877','EMP009'),
  (10,10,'2025-07-11 15:35:00',129.00,'+506 7000-9988','EMP010');

--Invoice.Products
INSERT INTO invoice_products (product_code, invoice_id, quantity) VALUES
  ('P001', 1, 2),
  ('P004', 1, 1),
  ('P003', 2, 1),
  ('P006', 2, 2),
  ('P009', 2, 1),
  ('P002', 3, 1),
  ('P005', 4, 3),
  ('P007', 5, 1),
  ('P010', 5, 2),
  ('P001', 6, 1),
  ('P008', 6, 1),
  ('P003', 7, 2),
  ('P006', 7, 1),
  ('P002', 8, 2),
  ('P009', 9, 1),
  ('P010', 9, 1),
  ('P005', 10,1);

