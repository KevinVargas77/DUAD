from db import conn
from psycopg2 import errors

# ---------- Users ----------
def create_user(data):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO lyfter_car_rental.users
                (first_name, last_name, email, username, user_password, birth_date, account_status)
                VALUES (%s, %s, %s, %s, %s, %s, COALESCE(%s, 'active'))
                RETURNING id;
            """, (
                data["first_name"], data["last_name"], data["email"],
                data["username"], data["password"], data["birth_date"],
                data.get("account_status")
            ))
            new_id = cur.fetchone()[0]
        conn.commit()
        return {"id": new_id}
    except errors.UniqueViolation:
        conn.rollback()
        raise
    except Exception:
        conn.rollback()
        raise

def update_user_status(user_id, new_status):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE lyfter_car_rental.users
            SET account_status = %s
            WHERE id = %s
            RETURNING id, account_status;
        """, (new_status, user_id))
        row = cur.fetchone()
    conn.commit()
    return row

def list_users(where_clauses, params):
    sql = "SELECT id, first_name, last_name, email, username, account_status, birth_date FROM lyfter_car_rental.users"
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " ORDER BY id ASC"
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()

# ---------- Automobiles ----------
def create_automobile(data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO lyfter_car_rental.automobiles
            (brand, model, manufacture_year, status)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (
            data["brand"], data["model"], data["manufacture_year"], data["status"]
        ))
        new_id = cur.fetchone()[0]
    conn.commit()
    return {"id": new_id}

def update_automobile_status(auto_id, new_status):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE lyfter_car_rental.automobiles
            SET status = %s
            WHERE id = %s
            RETURNING id, status;
        """, (new_status, auto_id))
        row = cur.fetchone()
    conn.commit()
    return row

def list_automobiles(where_clauses, params):
    sql = """
        SELECT id, brand, model, manufacture_year, status
        FROM lyfter_car_rental.automobiles
    """
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " ORDER BY id ASC"
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()

# ---------- Rentals ----------
def create_rent(data):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO lyfter_car_rental.rentals
            (user_id, automobile_id, rental_date, rental_status)
            VALUES (%s, %s, NOW(), 'active')
            RETURNING id;
        """, (
            data["user_id"], data["automobile_id"]
        ))
        new_id = cur.fetchone()[0]
    conn.commit()
    return {"id": new_id}

def complete_rental(rent_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE lyfter_car_rental.rentals
            SET rental_status = 'completed'
            WHERE id = %s
            RETURNING id, rental_status;
        """, (rent_id,))
        row = cur.fetchone()
    conn.commit()
    return row

def update_rental_status(rent_id, new_status):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE lyfter_car_rental.rentals
            SET rental_status = %s
            WHERE id = %s
            RETURNING id, rental_status;
        """, (new_status, rent_id))
        row = cur.fetchone()
    conn.commit()
    return row

def list_rentals(where_clauses, params):
    sql = """
        SELECT id, user_id, automobile_id, rental_date, rental_status
        FROM lyfter_car_rental.rentals
    """
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " ORDER BY id ASC"
    with conn.cursor() as cur:
        cur.execute(sql, params)