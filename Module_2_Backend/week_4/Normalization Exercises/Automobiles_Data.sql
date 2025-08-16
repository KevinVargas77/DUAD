PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS vehicle_models (
  model_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  make        TEXT    NOT NULL,
  model       TEXT    NOT NULL,
  model_year  INTEGER NOT NULL,
  UNIQUE (make, model, model_year)
);


CREATE TABLE IF NOT EXISTS vehicles (
  vin       TEXT    PRIMARY KEY,
  model_id  INTEGER NOT NULL,
  color     TEXT,
  FOREIGN KEY (model_id) REFERENCES vehicle_models(model_id)
);


CREATE TABLE IF NOT EXISTS owners (
  owner_id  INTEGER PRIMARY KEY,
  name      TEXT    NOT NULL,
  phone     TEXT    NOT NULL
);


CREATE TABLE IF NOT EXISTS insurance_policies (
  policy_number  TEXT    PRIMARY KEY,
  company        TEXT    NOT NULL
);


CREATE TABLE IF NOT EXISTS vehicle_owners (
  vin            TEXT    NOT NULL,
  owner_id       INTEGER NOT NULL,
  policy_number  TEXT    NOT NULL,
  PRIMARY KEY (vin, owner_id, policy_number),
  FOREIGN KEY (vin)            REFERENCES vehicles(vin),
  FOREIGN KEY (owner_id)       REFERENCES owners(owner_id),
  FOREIGN KEY (policy_number)  REFERENCES insurance_policies(policy_number)
);

-- INSERT DATA FROM PREVIOUS TABLE

PRAGMA foreign_keys = ON;

--Models
INSERT OR IGNORE INTO vehicle_models (make, model, model_year) VALUES
  ('Honda','Accord',  2003),
  ('Honda','CR-V',    2014),
  ('Chevrolet','Volt',2015);

-- Vehicles (VIN → model_id)
INSERT INTO vehicles (vin, model_id, color)
SELECT '1HGCM82633A', vm.model_id, 'Silver'
  FROM vehicle_models vm
WHERE vm.make='Honda' AND vm.model='Accord' AND vm.model_year=2003;

INSERT INTO vehicles (vin, model_id, color)
SELECT '5J6RM4H79EL', vm.model_id, 'Blue'
  FROM vehicle_models vm
WHERE vm.make='Honda' AND vm.model='CR-V' AND vm.model_year=2014;

INSERT INTO vehicles (vin, model_id, color)
SELECT '1G1RA6EH1FU', vm.model_id, 'Red'
  FROM vehicle_models vm
WHERE vm.make='Chevrolet' AND vm.model='Volt' AND vm.model_year=2015;

--Owners
INSERT OR IGNORE INTO owners (owner_id, name, phone) VALUES
  (101,'Alice',  '123-456-7890'),
  (102,'Bob',    '987-654-3210'),
  (103,'Claire', '555-123-4567'),
  (104,'Dave',   '111-222-3333');

-- Insurance
INSERT OR IGNORE INTO insurance_policies (policy_number, company) VALUES
  ('POL12345','ABC Insurance'),
  ('POL54321','XYZ Insurance'),
  ('POL67890','DEF Insurance'),
  ('POL98765','GHI Insurance');

--VIN–Owner–Policy
INSERT INTO vehicle_owners (vin, owner_id, policy_number) VALUES
  ('1HGCM82633A',101,'POL12345'),
  ('1HGCM82633A',102,'POL54321'),
  ('5J6RM4H79EL',103,'POL67890'),
  ('1G1RA6EH1FU',104,'POL98765');

--Query for testing 
SELECT
  v.vin,
  vm.make,
  vm.model,
  vm.model_year AS year,
  v.color,
  o.owner_id,
  o.name        AS owner_name,
  o.phone       AS owner_phone,
  ip.policy_number,
  ip.company    AS insurance_company
FROM vehicles v
JOIN vehicle_models vm       ON vm.model_id       = v.model_id
JOIN vehicle_owners  vo      ON vo.vin            = v.vin
JOIN owners         o        ON o.owner_id        = vo.owner_id
JOIN insurance_policies ip   ON ip.policy_number  = vo.policy_number
ORDER BY v.vin, o.owner_id;
