PRAGMA foreign_keys = ON;
--  Add buyer’s phone to invoices
ALTER TABLE invoices
  ADD COLUMN buyer_phone    TEXT;

-- Add cashier’s employee code to invoices
ALTER TABLE invoices
  ADD COLUMN employee_code  TEXT;
  
