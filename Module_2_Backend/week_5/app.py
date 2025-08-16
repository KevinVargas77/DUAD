from flask import Flask, request, jsonify
from db import conn   # <--- importas la conexión desde db.py
from psycopg2 import errors


app = Flask(__name__)


# ---------- Home ----------
@app.get("/")
def home():
    return "API funcionando!"


# ---------- Users ----------
@app.post("/users")
def create_user():
    data = request.get_json(force=True)
    required = ["first_name","last_name","email","username","password","birth_date"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error":"missing fields","fields":missing}), 400

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO lyfter_car_rental.users
                (first_name,last_name,email,username,user_password,birth_date,account_status)
                VALUES (%s,%s,%s,%s,%s,%s, COALESCE(%s,'active'))
                RETURNING id;
            """, (
                data["first_name"], data["last_name"], data["email"],
                data["username"], data["password"], data["birth_date"],
                data.get("account_status"),
            ))
            new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"id": new_id, "message": "user created"}), 201

    except errors.UniqueViolation:
        conn.rollback()
        return jsonify({"error": "email or username already exists"}), 409
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "internal error"}), 500


@app.patch("/users/<int:user_id>/status")
def update_user_status(user_id):
    data = request.get_json(force=True)
    new_status = data.get("status")

    allowed = {"active", "inactive", "delinquent"}
    if new_status not in allowed:
        return jsonify({"error": "invalid status", "allowed": sorted(list(allowed))}), 400

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE lyfter_car_rental.users
            SET account_status = %s
            WHERE id = %s
            RETURNING id, account_status;
        """, (new_status, user_id))
        row = cur.fetchone()
    conn.commit()

    if not row:
        return jsonify({"error": "user not found"}), 404

    return jsonify({"id": row[0], "status": row[1]}), 200


@app.get("/users")
def list_allowed():
    allowed = {"id","first_name","last_name","email","username","account_status","birth_date"}

    args = request.args
    where_clauses = [] 
    params = []

    for key, value in args.items():
        if key in allowed and value: 
            if key in {"first_name","last_name","email","username"}:
                where_clauses.append(f"{key} ILIKE %s")
                params.append(f"%{value}%")
            else:
                where_clauses.append(f"{key} = %s")
                params.append(value)

    sql = "SELECT id, first_name, last_name, email, username, account_status, birth_date FROM lyfter_car_rental.users"
    if where_clauses:
        sql += "WHERE" + "AND".join(where_clauses)
    sql += "ORDER BY id ASC"


    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall() 

    
    users = [
        {
            "id": r[0], "first_name": r[1], "last_name": r[2],
            "email": r[3], "username": r[4],
            "account_status": r[5], "birth_date": r[6].isoformat() if r[6] else None
        }
        for r in rows
    ]
    return jsonify(users), 200



# ---------- Automobiles ----------
@app.post("/automobiles")
def create_automobile():
    data = request.get_json(force=True)
    required = ["brand","model","manufacture_year","status"]
    missing = [f for f in required if not data.get(f)]
    if missing: return jsonify({"error":"missing fields","fields":missing}), 400

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO lyfter_car_rental.automobiles
            (brand,model,manufacture_year,status)
            VALUES (%s,%s,%s,%s)
            RETURNING id;
        """, (data["brand"], data["model"], data["manufacture_year"], data["status"]))
        new_id = cur.fetchone()[0]
    conn.commit()
    return jsonify({"id": new_id, "message": "automobile created"}), 201

@app.patch("/automobiles/<int:auto_id>/status")
def update_automobile_status(auto_id):
    data = request.get_json(force=True)
    new_status = data.get("status")
    allowed = {"available","rented","maintenance","unavailable"}
    if new_status not in allowed:
        return jsonify({"error":"invalid status","allowed":sorted(list(allowed))}), 400

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE lyfter_car_rental.automobiles
            SET status=%s WHERE id=%s
            RETURNING id, status;
        """, (new_status, auto_id))
        row = cur.fetchone()
    conn.commit()
    if not row: return jsonify({"error":"automobile not found"}), 404
    return jsonify({"id": row[0], "status": row[1]}), 200


@app.get("/automobiles")
def list_automobiles():
    allowed = {"id", "brand", "model", "manufacture_year", "status"}
    args = request.args
    where_clauses, params = [], []

    for key, value in args.items():
        if key in allowed and value:
            if key in {"brand", "model"}:
                where_clauses.append(f"{key} ILIKE %s")
                params.append(f"%{value}%")
            else:
                where_clauses.append(f"{key} = %s")
                params.append(value)

    sql = """
        SELECT id, brand, model, manufacture_year, status
        FROM lyfter_car_rental.automobiles
    """
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " ORDER BY id ASC"

    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    autos = [
        {
            "id": r[0],
            "brand": r[1],
            "model": r[2],
            "manufacture_year": r[3],
            "status": r[4],
        }
        for r in rows
    ]
    return jsonify(autos), 200



# ---------- Rentals ----------
@app.post("/new_rent")
def create_rent():
    data = request.get_json(force=True)
    required = ["user_id","automobile_id"]
    missing = [f for f in required if not data.get(f)]
    if missing: return jsonify({"error":"missing fields","fields":missing}), 400

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO lyfter_car_rental.rentals
            (user_id,automobile_id,rental_status)
            VALUES (%s,%s,'active')
            RETURNING id;
        """, (data["user_id"], data["automobile_id"]))
        rent_id = cur.fetchone()[0]
        cur.execute("""
            UPDATE lyfter_car_rental.automobiles
            SET status='rented' WHERE id=%s;
        """, (data["automobile_id"],))
    conn.commit()
    return jsonify({"id": rent_id, "message": "rent created"}), 201


@app.patch("/rentals/<int:rent_id>/complete")
def complete_rental(rent_id):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE lyfter_car_rental.rentals
                SET rental_status = 'completed'
                WHERE id = %s AND rental_status = 'active'
                RETURNING automobile_id;
            """, (rent_id,))
            row = cur.fetchone()
            if not row:
                return jsonify({"error": "rental not found or not active"}), 400
            automobile_id = row[0]

            cur.execute("""
                UPDATE lyfter_car_rental.automobiles
                SET status = 'available'
                WHERE id = %s
                RETURNING id, status;
            """, (automobile_id,))

        conn.commit()
        return jsonify({"rental_id": rent_id, "automobile_id": automobile_id, "message": "rental completed"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.patch("/rentals/<int:rent_id>/status")
def update_rental_status(rent_id):
    data = request.get_json(force=True)
    new_status = data.get("status")

    allowed = {"active", "completed", "cancelled"}
    if new_status not in allowed:
        return jsonify({"error": "invalid status", "allowed": sorted(list(allowed))}), 400

    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE lyfter_car_rental.rentals
                SET rental_status = %s
                WHERE id = %s
                RETURNING id, rental_status;
            """, (new_status, rent_id))
            row = cur.fetchone()
        conn.commit()

        if not row:
            return jsonify({"error": "rental not found"}), 404

        return jsonify({"id": row[0], "status": row[1]}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.get("/rentals")
def list_rentals():
    allowed = {"id", "user_id", "automobile_id", "rental_date", "rental_status"}
    args = request.args
    where_clauses, params = [], []

    for key, value in args.items():
        if key in allowed and value:
            if key in {"rental_status"}:
                where_clauses.append(f"{key} ILIKE %s")
                params.append(f"%{value}%")
            else:
                where_clauses.append(f"{key} = %s")
                params.append(value)

    sql = """
        SELECT id, user_id, automobile_id, rental_date, rental_status
        FROM lyfter_car_rental.rentals
    """
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " ORDER BY id ASC"

    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    rentals = [
        {
            "id": r[0],
            "user_id": r[1],
            "automobile_id": r[2],
            "rental_date": r[3].isoformat() if r[3] else None,
            "rental_status": r[4],
        }
        for r in rows
    ]
    return jsonify(rentals), 200


if __name__ == "__main__":
    app.run(debug=True)
