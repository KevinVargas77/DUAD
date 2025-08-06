PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS vehicles (
  vin    TEXT    PRIMARY KEY,
  make   TEXT    NOT NULL,
  model  TEXT    NOT NULL,
  year   INTEGER,
  color  TEXT
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

-- Vehicles
INSERT INTO vehicles (vin, make, model, year, color) VALUES
  ('1HGCM82633A','Honda','Accord', 2003,'Silver'),
  ('5J6RM4H79EL','Honda','CR-V',   2014,'Blue'),
  ('1G1RA6EH1FU','Chevrolet','Volt',2015,'Red');

-- Owners
INSERT INTO owners (owner_id, name, phone) VALUES
  (101,'Alice',  '123-456-7890'),
  (102,'Bob',    '987-654-3210'),
  (103,'Claire', '555-123-4567'),
  (104,'Dave',   '111-222-3333');

-- Insurance Policies
INSERT INTO insurance_policies (policy_number, company) VALUES
  ('POL12345','ABC Insurance'),
  ('POL54321','XYZ Insurance'),
  ('POL67890','DEF Insurance'),
  ('POL98765','GHI Insurance');

-- Vehicle_Owners
INSERT INTO vehicle_owners (vin, owner_id, policy_number) VALUES
  ('1HGCM82633A',101,'POL12345'),
  ('1HGCM82633A',102,'POL54321'),
  ('5J6RM4H79EL',103,'POL67890'),
  ('1G1RA6EH1FU',104,'POL98765');

-- QUERY FOR TESTING
SELECT
  v.vin,
  v.make,
  v.model,
  v.year,
  v.color,
  o.owner_id,
  o.name      AS owner_name,
  o.phone     AS owner_phone,
  ip.policy_number,
  ip.company  AS insurance_company
FROM vehicles AS v
JOIN vehicle_owners AS vo ON vo.vin = v.vin
JOIN owners         AS o  ON o.owner_id        = vo.owner_id
JOIN insurance_policies AS ip ON ip.policy_number = vo.policy_number
ORDER BY v.vin, o.owner_id;



