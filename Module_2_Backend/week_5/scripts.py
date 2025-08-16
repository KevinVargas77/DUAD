import os
import csv
from datetime import date
from db import conn

##backups script
BASE_DIR = "db_backups"
today = date.today().isoformat()          # 2025-08-15
BACKUP_DIR = os.path.join(BASE_DIR, today)
os.makedirs(BACKUP_DIR, exist_ok=True)

tables = {
    "lyfter_car_rental.users": "users",
    "lyfter_car_rental.automobiles": "automobiles",
    "lyfter_car_rental.rentals": "rentals",
}

with conn.cursor() as cur:
    for full_table, base in tables.items():
        cur.execute(f"SELECT * FROM {full_table}")
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]

        out_path = os.path.join(BACKUP_DIR, f"{base}_backup_{today}.csv")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)

conn.close()
print("Backups guardados en:", BACKUP_DIR)


##connection validation and health check

# health_check.py
from db import conn

SCHEMA = "lyfter_car_rental"
TABLES = ["users", "automobiles", "rentals"]

def table_exists(cur, schema, table):
    cur.execute("""
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = %s AND table_name = %s
        """, (schema, table))
    return cur.fetchone() is not None

try:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        for t in TABLES:
            if not table_exists(cur, SCHEMA, t):
                print(f"DB ERROR. Missing table: {t}")
                raise SystemExit(1)

        cur.execute(f"""
            SELECT COUNT(*) FROM {SCHEMA}.automobiles
            WHERE status = 'available'
        """)
        available = cur.fetchone()[0]
        if available < 1:
            print("DB ERROR. No available automobiles")
            raise SystemExit(1)

    print("DB OK. System running normally")
    conn.close()

except Exception:
    print("DB ERROR. Connection or query failed")
    try:
        conn.close()
    except Exception:
        pass
    raise SystemExit(1)


##faker script to create table entries 

from db import conn
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

SCHEMA = "lyfter_car_rental"

def rand_date(start_year=2023):
    start = datetime(start_year, 1, 1)
    end = datetime.now()
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days),
                             seconds=random.randint(0, 86400))

try:
    with conn.cursor() as cur:

        users = []
        for _ in range(200):
            first = fake.first_name()
            last = fake.last_name()
            email = fake.unique.email()
            username = fake.unique.user_name()
            pwd = fake.password(length=10)
            birth = fake.date_of_birth(minimum_age=18, maximum_age=75).isoformat()
            status = random.choice(["active", "inactive", "delinquent"])
            users.append((first, last, email, username, pwd, birth, status))

        cur.executemany(
            f"""
            INSERT INTO {SCHEMA}.users
            (first_name, last_name, email, username, user_password, birth_date, account_status)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            users,
        )


        brands = ["Toyota","Honda","Ford","Chevrolet","Nissan","Hyundai","Kia","VW","Mazda","Subaru"]
        models = ["Corolla","Civic","Focus","Cruze","Sentra","Elantra","Rio","Jetta","Mazda3","Impreza",
                  "Camry","Accord","Fusion","Malibu","Altima","Sonata","Optima","Passat","CX-5","Forester",
                  "RAV4","CR-V","Escape","Equinox","Rogue","Tucson","Sportage","Tiguan","CX-30","Outback"]
        autos = []
        for _ in range(100):
            autos.append((
                random.choice(brands),
                random.choice(models),
                random.randint(2005, 2024),
                random.choice(["available","rented","maintenance","unavailable"])
            ))

        cur.executemany(
            f"""
            INSERT INTO {SCHEMA}.automobiles
            (brand, model, manufacture_year, status)
            VALUES (%s,%s,%s,%s)
            """,
            autos,
        )


        cur.execute(f"SELECT id FROM {SCHEMA}.users")
        user_ids = [r[0] for r in cur.fetchall()]

        cur.execute(f"SELECT id FROM {SCHEMA}.automobiles")
        auto_ids = [r[0] for r in cur.fetchall()]


        rentals = []
        for _ in range(random.randint(50, 150)):
            uid = random.choice(user_ids)
            aid = random.choice(auto_ids)
            rdate = rand_date().isoformat(sep=" ", timespec="seconds")
            rstatus = random.choice(["active", "completed", "cancelled"])
            rentals.append((uid, aid, rdate, rstatus))

        cur.executemany(
            f"""
            INSERT INTO {SCHEMA}.rentals
            (user_id, automobile_id, rental_date, rental_status)
            VALUES (%s,%s,%s,%s)
            """,
            rentals,
        )


        cur.execute(f"""
            UPDATE {SCHEMA}.automobiles
            SET status = 'rented'
            WHERE id IN (
                SELECT DISTINCT automobile_id
                FROM {SCHEMA}.rentals
                WHERE rental_status = 'active'
            )
        """)

        cur.execute(f"""
            UPDATE {SCHEMA}.automobiles
            SET status = 'available'
            WHERE id NOT IN (
                SELECT DISTINCT automobile_id
                FROM {SCHEMA}.rentals
                WHERE rental_status = 'active'
            )
            AND status = 'rented'
        """)

    conn.commit()
    print("Seed completed: 200 users, 100 automobiles, 50–150 rentals.")

except Exception as e:
    conn.rollback()
    print("Seed failed:", str(e))
finally:
    conn.close()
