CREATE TABLE IF NOT EXISTS users (
  id         BIGSERIAL PRIMARY KEY,
  name       TEXT NOT NULL,
  email      TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
  id         BIGSERIAL PRIMARY KEY,
  name       TEXT NOT NULL,
  price      NUMERIC(12,2) NOT NULL CHECK (price >= 0),
  stock      INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
  version    INTEGER NOT NULL DEFAULT 0           -- optimistic lock
);

CREATE TABLE IF NOT EXISTS invoices (
  id         BIGSERIAL PRIMARY KEY,
  user_id    BIGINT NOT NULL REFERENCES users(id),
  status     TEXT NOT NULL DEFAULT 'Pending',     -- Pending | Completed | Cancelled | Returned
  returned   BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS invoice_details (
  id          BIGSERIAL PRIMARY KEY,
  invoice_id  BIGINT NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  product_id  BIGINT NOT NULL REFERENCES products(id),
  quantity    INTEGER NOT NULL CHECK (quantity > 0),
  delivered   BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_invoice_details_invoice ON invoice_details(invoice_id);
CREATE INDEX IF NOT EXISTS idx_invoice_details_product  ON invoice_details(product_id);

-- ------------------------------------------------------------------
-- Helpers
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION assert_user_exists(_user_id BIGINT) RETURNS VOID AS $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM users WHERE id = _user_id) THEN
    RAISE EXCEPTION 'User % does not exist', _user_id;
  END IF;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------------
-- A) Single-product purchase (atomic)
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION purchase_one(_user_id BIGINT, _product_id BIGINT, _qty INTEGER)
RETURNS BIGINT AS $$
DECLARE
  _invoice_id BIGINT;
BEGIN
  PERFORM assert_user_exists(_user_id);

  -- Atomically decrement stock only if sufficient
  UPDATE products
     SET stock = stock - _qty,
         version = version + 1
   WHERE id = _product_id
     AND stock >= _qty
  RETURNING id INTO _product_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Insufficient stock or product not found (product_id=%)', _product_id;
  END IF;

  INSERT INTO invoices (user_id, status)
  VALUES (_user_id, 'Completed')
  RETURNING id INTO _invoice_id;

  INSERT INTO invoice_details (invoice_id, product_id, quantity, delivered)
  VALUES (_invoice_id, _product_id, _qty, TRUE);

  RETURN _invoice_id;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------------
-- B1) Return the entire invoice
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION return_invoice(_invoice_id BIGINT)
RETURNS VOID AS $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM invoices WHERE id = _invoice_id) THEN
    RAISE EXCEPTION 'Invoice % does not exist', _invoice_id;
  END IF;

  -- Return stock for all items in the invoice
  UPDATE products p
     SET stock = p.stock + d.sum_qty
    FROM (
      SELECT product_id, SUM(quantity) AS sum_qty
      FROM invoice_details
      WHERE invoice_id = _invoice_id
      GROUP BY product_id
    ) d
   WHERE p.id = d.product_id;

  -- Mark invoice as Returned
  UPDATE invoices SET returned = TRUE, status = 'Returned'
  WHERE id = _invoice_id;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------------
-- B2) Return a single product from an invoice
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION return_invoice_item(_invoice_id BIGINT, _product_id BIGINT)
RETURNS VOID AS $$
DECLARE
  _sum_qty INTEGER;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM invoices WHERE id = _invoice_id) THEN
    RAISE EXCEPTION 'Invoice % does not exist', _invoice_id;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM invoice_details WHERE invoice_id = _invoice_id AND product_id = _product_id) THEN
    RAISE EXCEPTION 'Invoice detail not found for invoice % and product %', _invoice_id, _product_id;
  END IF;

  SELECT COALESCE(SUM(quantity),0) INTO _sum_qty
  FROM invoice_details
  WHERE invoice_id = _invoice_id AND product_id = _product_id;

  UPDATE products SET stock = stock + _sum_qty WHERE id = _product_id;

  -- Business rule: optionally set Returned only if *all* items are returned.
  UPDATE invoices SET returned = TRUE, status = 'Returned'
  WHERE id = _invoice_id;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------------
-- C) Multi-item purchase (all-or-nothing)
-- items_json example: '[{"product_id":1,"qty":2},{"product_id":3,"qty":1}]'
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION purchase_multi(_user_id BIGINT, items_json JSONB)
RETURNS BIGINT AS $$
DECLARE
  _invoice_id BIGINT;
  _insufficient_count INTEGER;
BEGIN
  PERFORM assert_user_exists(_user_id);

  -- Validate stock for all requested items
  SELECT COUNT(*) INTO _insufficient_count
  FROM (
    SELECT (j->>'product_id')::BIGINT AS product_id,
           (j->>'qty')::INTEGER     AS qty
    FROM JSONB_ARRAY_ELEMENTS(items_json) AS j
  ) x
  JOIN products p ON p.id = x.product_id
  WHERE p.stock < x.qty;

  IF _insufficient_count > 0 THEN
    RAISE EXCEPTION 'Insufficient stock for one or more products';
  END IF;

  -- Create invoice
  INSERT INTO invoices (user_id, status) VALUES (_user_id, 'Completed')
  RETURNING id INTO _invoice_id;

  -- Insert details
  INSERT INTO invoice_details (invoice_id, product_id, quantity, delivered)
  SELECT _invoice_id,
         (j->>'product_id')::BIGINT,
         (j->>'qty')::INTEGER,
         TRUE
  FROM JSONB_ARRAY_ELEMENTS(items_json) AS j;

  -- Decrement stock in bulk
  UPDATE products p
     SET stock = p.stock - x.qty,
         version = p.version + 1
    FROM (
      SELECT (j->>'product_id')::BIGINT AS product_id,
             (j->>'qty')::INTEGER     AS qty
      FROM JSONB_ARRAY_ELEMENTS(items_json) AS j
    ) x
   WHERE p.id = x.product_id;

  RETURN _invoice_id;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------------
-- D) Cancel a Pending invoice (return only not-delivered items)
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION cancel_pending_invoice(_invoice_id BIGINT)
RETURNS VOID AS $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM invoices WHERE id = _invoice_id AND status = 'Pending') THEN
    RAISE EXCEPTION 'Invoice % must be in Pending status to cancel', _invoice_id;
  END IF;

  -- Return stock only for items not delivered
  UPDATE products p
     SET stock = p.stock + d.sum_qty
    FROM (
      SELECT product_id, SUM(quantity) AS sum_qty
      FROM invoice_details
      WHERE invoice_id = _invoice_id AND delivered = FALSE
      GROUP BY product_id
    ) d
   WHERE p.id = d.product_id;

  -- Mark invoice as Cancelled
  UPDATE invoices SET status = 'Cancelled'
   WHERE id = _invoice_id;
END;
$$ LANGUAGE plpgsql;

-- ------------------------------------------------------------------
-- E) Optimistic locking purchase (expected product version)
-- ------------------------------------------------------------------
CREATE OR REPLACE FUNCTION try_buy_with_optimistic_lock(
  _user_id BIGINT,
  _product_id BIGINT,
  _qty INTEGER,
  _expected_version INTEGER
) RETURNS BIGINT AS $$
DECLARE
  _invoice_id BIGINT;
  _updated_id BIGINT;
BEGIN
  PERFORM assert_user_exists(_user_id);

  UPDATE products
     SET stock = stock - _qty,
         version = version + 1
   WHERE id = _product_id
     AND stock >= _qty
     AND version = _expected_version
  RETURNING id INTO _updated_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Concurrent update detected or insufficient stock (product_id=%, expected_version=%)',
      _product_id, _expected_version;
  END IF;

  INSERT INTO invoices (user_id, status)
  VALUES (_user_id, 'Completed')
  RETURNING id INTO _invoice_id;

  INSERT INTO invoice_details (invoice_id, product_id, quantity, delivered)
  VALUES (_invoice_id, _product_id, _qty, TRUE);

  RETURN _invoice_id;
END;
$$ LANGUAGE plpgsql;
