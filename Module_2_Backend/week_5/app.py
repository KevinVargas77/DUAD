from flask import Flask, request, jsonify
from repositories import (
    create_user, update_user_status, list_users,
    create_automobile, update_automobile_status, list_automobiles,
    create_rent, complete_rental, update_rental_status, list_rentals
)
from psycopg2 import errors

app = Flask(__name__)


# ---------- Home ----------
@app.get("/")
def home():
    return "API funcionando!"


# ---------- Users ----------
@app.post("/users")
def create_user_endpoint():
    data = request.get_json(force=True)
    required = ["first_name", "last_name", "email", "username", "password", "birth_date"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": "missing fields", "fields": missing}), 400
    try:
        result = create_user(data)
        return jsonify({"id": result["id"], "message": "user created"}), 201
    except errors.UniqueViolation:
        return jsonify({"error": "email or username already exists"}), 409
    except Exception:
        return jsonify({"error": "internal error"}), 500


@app.patch("/users/<int:user_id>/status")
def update_user_status_endpoint(user_id):
    data = request.get_json(force=True)
    new_status = data.get("status")
    allowed = {"active", "inactive", "delinquent"}
    if new_status not in allowed:
        return jsonify({"error": "invalid status", "allowed": sorted(list(allowed))}), 400
    row = update_user_status(user_id, new_status)
    if not row:
        return jsonify({"error": "user not found"}), 404
    return jsonify({"id": row[0], "status": row[1]}), 200


@app.get("/users")
def list_users_endpoint():
    allowed = {"id", "first_name", "last_name", "email", "username", "account_status", "birth_date"}
    args = request.args
    where_clauses, params = [], []
    for key, value in args.items():
        if key in allowed and value:
            if key in {"first_name", "last_name", "email", "username"}:
                where_clauses.append(f"{key} ILIKE %s")
                params.append(f"%{value}%")
            else:
                where_clauses.append(f"{key} = %s")
                params.append(value)
    rows = list_users(where_clauses, params)
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
def create_automobile_endpoint():
    data = request.get_json(force=True)
    required = ["brand", "model", "manufacture_year", "status"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": "missing fields", "fields": missing}), 400
    result = create_automobile(data)
    return jsonify({"id": result["id"], "message": "automobile created"}), 201


@app.patch("/automobiles/<int:auto_id>/status")
def update_automobile_status_endpoint(auto_id):
    data = request.get_json(force=True)
    new_status = data.get("status")
    allowed = {"available", "rented", "maintenance", "unavailable"}
    if new_status not in allowed:
        return jsonify({"error": "invalid status", "allowed": sorted(list(allowed))}), 400
    row = update_automobile_status(auto_id, new_status)
    if not row:
        return jsonify({"error": "automobile not found"}), 404
    return jsonify({"id": row[0], "status": row[1]}), 200


@app.get("/automobiles")
def list_automobiles_endpoint():
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
    rows = list_automobiles(where_clauses, params)
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
def create_rent_endpoint():
    data = request.get_json(force=True)
    required = ["user_id", "automobile_id"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": "missing fields", "fields": missing}), 400
    result = create_rent(data)
    return jsonify({"id": result["id"], "message": "rent created"}), 201


@app.patch("/rentals/<int:rent_id>/complete")
def complete_rental_endpoint(rent_id):
    row = complete_rental(rent_id)
    if not row:
        return jsonify({"error": "rental not found or not active"}), 400
    return jsonify({"rental_id": rent_id, "automobile_id": row[0], "message": "rental completed"}), 200


@app.patch("/rentals/<int:rent_id>/status")
def update_rental_status_endpoint(rent_id):
    data = request.get_json(force=True)
    new_status = data.get("status")
    allowed = {"active", "completed", "cancelled"}
    if new_status not in allowed:
        return jsonify({"error": "invalid status", "allowed": sorted(list(allowed))}), 400
    row = update_rental_status(rent_id, new_status)
    if not row:
        return jsonify({"error": "rental not found"}), 404
    return jsonify({"id": row[0], "status": row[1]}), 200


@app.get("/rentals")
def list_rentals_endpoint():
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
    rows = list_rentals(where_clauses, params)
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
