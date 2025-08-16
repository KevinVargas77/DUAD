--create a new schema 
CREATE SCHEMA lyfter_car_rental;

--create table users 
CREATE TABLE IF NOT EXISTS lyfter_car_rental.users (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    user_password TEXT NOT NULL,
    birth_date DATE NOT NULL,
    account_status TEXT DEFAULT 'activo'
);

--Insert data into users table
INSERT INTO lyfter_car_rental.users
(first_name, last_name, email, username, user_password, birth_date, account_status)
VALUES
('Juan', 'Pérez', 'juan.perez1@example.com', 'juanp1', 'pass123', '1990-01-15', 'activo'),
('María', 'Gómez', 'maria.gomez2@example.com', 'mariag2', 'pass234', '1992-02-20', 'activo'),
('Carlos', 'López', 'carlos.lopez3@example.com', 'carlitos3', 'pass345', '1988-03-10', 'inactivo'),
('Laura', 'Martínez', 'laura.martinez4@example.com', 'lauram4', 'pass456', '1995-04-05', 'activo'),
('Pedro', 'Hernández', 'pedro.hernandez5@example.com', 'pedroh5', 'pass567', '1989-05-25', 'activo'),
('Ana', 'Rodríguez', 'ana.rodriguez6@example.com', 'anar6', 'pass678', '1991-06-12', 'inactivo'),
('Sofía', 'Torres', 'sofia.torres7@example.com', 'sofiat7', 'pass789', '1993-07-19', 'activo'),
('Miguel', 'Flores', 'miguel.flores8@example.com', 'miguelf8', 'pass890', '1987-08-22', 'activo'),
('Valeria', 'Jiménez', 'valeria.jimenez9@example.com', 'valj9', 'pass901', '1996-09-30', 'activo'),
('Andrés', 'Castro', 'andres.castro10@example.com', 'andresc10', 'pass012', '1990-10-18', 'activo'),
('Lucía', 'Méndez', 'lucia.mendez11@example.com', 'luciam11', 'pass1234', '1994-11-11', 'inactivo'),
('Diego', 'Vargas', 'diego.vargas12@example.com', 'diegov12', 'pass2234', '1986-12-03', 'activo'),
('Camila', 'Morales', 'camila.morales13@example.com', 'camim13', 'pass3234', '1997-01-09', 'activo'),
('Fernando', 'Suárez', 'fernando.suarez14@example.com', 'fer14', 'pass4234', '1992-02-14', 'activo'),
('Isabella', 'Romero', 'isabella.romero15@example.com', 'isa15', 'pass5234', '1991-03-21', 'activo'),
('Ricardo', 'Navarro', 'ricardo.navarro16@example.com', 'rick16', 'pass6234', '1993-04-27', 'inactivo'),
('Gabriela', 'Cruz', 'gabriela.cruz17@example.com', 'gaby17', 'pass7234', '1988-05-05', 'activo'),
('Javier', 'Silva', 'javier.silva18@example.com', 'jav18', 'pass8234', '1990-06-16', 'activo'),
('Paula', 'Ortega', 'paula.ortega19@example.com', 'pau19', 'pass9234', '1994-07-24', 'activo'),
('Hugo', 'Delgado', 'hugo.delgado20@example.com', 'hugo20', 'pass1334', '1995-08-08', 'activo'),
('Daniela', 'Santos', 'daniela.santos21@example.com', 'dani21', 'pass2334', '1989-09-09', 'activo'),
('Felipe', 'Paredes', 'felipe.paredes22@example.com', 'feli22', 'pass3334', '1991-10-02', 'activo'),
('Natalia', 'Campos', 'natalia.campos23@example.com', 'nat23', 'pass4334', '1993-11-12', 'inactivo'),
('Sebastián', 'Ibarra', 'sebastian.ibarra24@example.com', 'sebas24', 'pass5334', '1987-12-28', 'activo'),
('Mariana', 'Molina', 'mariana.molina25@example.com', 'mary25', 'pass6334', '1996-01-19', 'activo'),
('Tomás', 'Reyes', 'tomas.reyes26@example.com', 'tom26', 'pass7334', '1994-02-22', 'activo'),
('Alejandra', 'Ríos', 'alejandra.rios27@example.com', 'ale27', 'pass8334', '1992-03-03', 'activo'),
('Cristian', 'Peña', 'cristian.pena28@example.com', 'cris28', 'pass9334', '1990-04-14', 'activo'),
('Pablo', 'Aguilar', 'pablo.aguilar29@example.com', 'pablo29', 'pass1434', '1989-05-25', 'activo'),
('Mónica', 'Vega', 'monica.vega30@example.com', 'moni30', 'pass2434', '1995-06-06', 'inactivo'),
('Esteban', 'Fuentes', 'esteban.fuentes31@example.com', 'esteban31', 'pass3434', '1991-07-17', 'activo'),
('Carmen', 'Salazar', 'carmen.salazar32@example.com', 'carmen32', 'pass4434', '1993-08-28', 'activo'),
('Iván', 'León', 'ivan.leon33@example.com', 'ivan33', 'pass5434', '1988-09-09', 'activo'),
('Luisa', 'Carrillo', 'luisa.carrillo34@example.com', 'luisa34', 'pass6434', '1996-10-10', 'activo'),
('Rodrigo', 'Figueroa', 'rodrigo.figueroa35@example.com', 'rodrigo35', 'pass7434', '1994-11-21', 'activo'),
('Patricia', 'Mendoza', 'patricia.mendoza36@example.com', 'patricia36', 'pass8434', '1992-12-12', 'activo'),
('Mauricio', 'Cortés', 'mauricio.cortes37@example.com', 'mauricio37', 'pass9434', '1987-01-23', 'activo'),
('Sandra', 'Herrera', 'sandra.herrera38@example.com', 'sandra38', 'pass1534', '1990-02-14', 'inactivo'),
('Óscar', 'Acosta', 'oscar.acosta39@example.com', 'oscar39', 'pass2534', '1995-03-25', 'activo'),
('Beatriz', 'Ramos', 'beatriz.ramos40@example.com', 'bea40', 'pass3534', '1993-04-04', 'activo'),
('Elena', 'Guerrero', 'elena.guerrero41@example.com', 'elena41', 'pass4534', '1991-05-15', 'activo'),
('Raúl', 'Palacios', 'raul.palacios42@example.com', 'raul42', 'pass5534', '1989-06-26', 'activo'),
('Fabiola', 'Vargas', 'fabiola.vargas43@example.com', 'fabiola43', 'pass6534', '1996-07-07', 'activo'),
('Alberto', 'Lara', 'alberto.lara44@example.com', 'alberto44', 'pass7534', '1994-08-18', 'activo'),
('Rosa', 'Montoya', 'rosa.montoya45@example.com', 'rosa45', 'pass8534', '1992-09-29', 'activo'),
('Marcos', 'Pinto', 'marcos.pinto46@example.com', 'marcos46', 'pass9534', '1990-10-10', 'activo'),
('Alicia', 'Campos', 'alicia.campos47@example.com', 'alicia47', 'pass1634', '1988-11-21', 'activo'),
('Jorge', 'Arce', 'jorge.arce48@example.com', 'jorge48', 'pass2634', '1995-12-01', 'activo'),
('Verónica', 'Paredes', 'veronica.paredes49@example.com', 'vero49', 'pass3634', '1993-01-12', 'activo'),
('Héctor', 'Rivas', 'hector.rivas50@example.com', 'hector50', 'pass4634', '1991-02-23', 'activo');

-- create table automobiles

CREATE TABLE lyfter_car_rental.automobiles (
    id SERIAL PRIMARY KEY,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    manufacture_year INT NOT NULL,
    status TEXT DEFAULT 'available'
);

-- Insert data into automobiles table
INSERT INTO lyfter_car_rental.automobiles
(brand, model, manufacture_year, status)
VALUES
('Toyota', 'Corolla', 2018, 'available'),
('Honda', 'Civic', 2019, 'available'),
('Ford', 'Focus', 2017, 'rented'),
('Chevrolet', 'Cruze', 2020, 'available'),
('Nissan', 'Sentra', 2016, 'maintenance'),
('Hyundai', 'Elantra', 2019, 'available'),
('Kia', 'Rio', 2018, 'available'),
('Volkswagen', 'Jetta', 2020, 'available'),
('Mazda', 'Mazda3', 2021, 'available'),
('Subaru', 'Impreza', 2017, 'rented'),
('Toyota', 'Camry', 2018, 'available'),
('Honda', 'Accord', 2019, 'available'),
('Ford', 'Fusion', 2020, 'available'),
('Chevrolet', 'Malibu', 2017, 'available'),
('Nissan', 'Altima', 2018, 'rented'),
('Hyundai', 'Sonata', 2019, 'available'),
('Kia', 'Optima', 2020, 'available'),
('Volkswagen', 'Passat', 2018, 'maintenance'),
('Mazda', 'CX-5', 2019, 'available'),
('Subaru', 'Forester', 2020, 'available'),
('Toyota', 'RAV4', 2021, 'available'),
('Honda', 'CR-V', 2017, 'rented'),
('Ford', 'Escape', 2018, 'available'),
('Chevrolet', 'Equinox', 2019, 'available'),
('Nissan', 'Rogue', 2020, 'available'),
('Hyundai', 'Tucson', 2018, 'available'),
('Kia', 'Sportage', 2019, 'available'),
('Volkswagen', 'Tiguan', 2020, 'available'),
('Mazda', 'CX-9', 2017, 'maintenance'),
('Subaru', 'Outback', 2018, 'available'),
('Toyota', 'Highlander', 2019, 'available'),
('Honda', 'Pilot', 2020, 'available'),
('Ford', 'Explorer', 2021, 'available'),
('Chevrolet', 'Traverse', 2018, 'available'),
('Nissan', 'Murano', 2019, 'rented'),
('Hyundai', 'Santa Fe', 2020, 'available'),
('Kia', 'Sorento', 2017, 'available'),
('Volkswagen', 'Atlas', 2018, 'available'),
('Mazda', 'MX-5', 2019, 'available'),
('Subaru', 'Ascent', 2020, 'maintenance'),
('Toyota', 'Prius', 2018, 'available'),
('Honda', 'Fit', 2019, 'available'),
('Ford', 'Fiesta', 2020, 'available'),
('Chevrolet', 'Spark', 2017, 'available'),
('Nissan', 'Versa', 2018, 'available'),
('Hyundai', 'Accent', 2019, 'available'),
('Kia', 'Soul', 2020, 'rented'),
('Volkswagen', 'Golf', 2017, 'available'),
('Mazda', 'CX-30', 2018, 'available'),
('Subaru', 'Crosstrek', 2019, 'available');


-- create rental table 

CREATE TABLE lyfter_car_rental.rentals (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    automobile_id INT NOT NULL,
    rental_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rental_status TEXT DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES lyfter_car_rental.users (id),
    FOREIGN KEY (automobile_id) REFERENCES lyfter_car_rental.automobiles (id)
);

-- insert sample rentals with varied dates
INSERT INTO lyfter_car_rental.rentals (user_id, automobile_id, rental_date, rental_status)
VALUES
(1, 3, '2025-01-15 10:30:00', 'active'),
(2, 5, '2025-02-02 14:45:00', 'completed'),
(4, 7, '2024-12-20 09:15:00', 'active'),
(6, 2, '2024-11-10 16:50:00', 'cancelled'),
(8, 1, '2024-10-05 08:05:00', 'completed'),
(10, 4, '2025-01-01 12:00:00', 'active'),
(12, 9, '2024-09-25 18:30:00', 'completed'),
(15, 6, '2024-08-14 11:10:00', 'cancelled'),
(20, 8, '2024-07-30 15:40:00', 'active'),
(25, 10, '2024-06-18 07:25:00', 'completed');


