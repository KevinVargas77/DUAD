--a. Add a new user
INSERT INTO lyfter_car_rental.users
(first_name, last_name, email, username, user_password, birth_date, account_status)
VALUES 
('Kevin', 'Restrepo', 'kevin.restrepo@example.com', 'kevinr', 'clave_segura_123', '1995-08-14', 'activo');

--b. Add a new car 
INSERT INTO lyfter_car_rental.automobiles
(brand, model, manufacture_year, status)
VALUES
('Toyota', 'Yaris', 2023, 'available');

-- Verify the users list 
SELECT * 
FROM lyfter_car_rental.users 
ORDER BY id DESC;

--c.Change the user status
UPDATE lyfter_car_rental.users
SET account_status = 'inactive'
WHERE id = 51; 

-- verify if the user status changed 
SELECT account_status
FROM lyfter_car_rental.users
WHERE id = 51;

--d.Change the automobile status
UPDATE lyfter_car_rental.automobiles
SET status = 'maintenance'
WHERE id = 10; -- Cambia el ID del auto

-- Verify if the automobile status changed
SELECT status
FROM lyfter_car_rental.automobiles 
WHERE id = 10;

--e. verify which cars are 'available' to create the rent
SELECT id,status
FROM lyfter_car_rental.automobiles 
WHERE status = 'available'

--e. create a new car rent 
INSERT INTO lyfter_car_rental.rentals
(user_id, automobile_id, rental_status)
VALUES
(47, 27, 'active'); 

UPDATE lyfter_car_rental.automobiles
SET status = 'rented'
WHERE id = 27;


-- Verify if the new rent is active
SELECT *
FROM lyfter_car_rental.rentals
WHERE rental_status = 'active' AND 
automobile_id = 27;

--f.1.update the rental status 
UPDATE lyfter_car_rental.rentals
SET rental_status = 'completed'
WHERE id = 11; 

--f.2.and change the automobile status 
UPDATE lyfter_car_rental.automobiles
SET status = 'available'
WHERE id = (
    SELECT automobile_id 
    FROM lyfter_car_rental.rentals
    WHERE id = 11
);

--g. setup a car status as 'unavailable'
SELECT *
FROM lyfter_car_rental.automobiles
WHERE status "maintenance"

UPDATE lyfter_car_rental.automobiles
SET status = 'unavailable'
WHERE id = 29;

--h.1. rented cars list
SELECT * 
FROM lyfter_car_rental.automobiles
WHERE status = 'rented';

--h.2. available cars list
SELECT * 
FROM lyfter_car_rental.automobiles
WHERE status = 'available';