
# flask_rs256_fruits_api

## Quickstart

1) **Create & activate venv**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

2) **Install deps**
```bash
pip install -r requirements.txt
```

3) **Configure environment**
- Copy `.env.example` in the api folder and rename it as `.env`and adjust values.
- Set `DATABASE_URL` to your Postgres URL, or use SQLite for quick tests.

4) **Generate RSA keys (for RS256)**
Run this command in your project folder:
```bash
python generate_keys.py
```
This will automatically create `private.pem` and `public.pem` for JWT authentication.

5) **Run the API**
```bash
python app.py
# or
python -m flask --app app run --host=0.0.0.0 --port=5000 --debug
```

6) **Smoke test**
```bash
curl http://127.0.0.1:5000/liveness
```

> The server auto-creates tables on first run.

---

## Role matrix

| Endpoint                       | Admin                                   | User                |
| ------------------------------ | --------------------------------------- | ------------------- |
| **POST /register**             | Yes (creates user; default role = user) | Yes (self‑register) |
| **POST /login**                | Yes                                     | Yes                 |
| **GET /me**                    | Yes                                     | Yes                 |
| **POST /refresh-token**        | Yes                                     | Yes                 |
| **GET /products**              | Yes                                     | Yes                 |
| **POST /products**             | Yes                                     | No                  |
| **PUT /products/\:id**         | Yes                                     | No                  |
| **DELETE /products/\:id**      | Yes                                     | No                  |
| **POST /purchase**             | Yes                                     | Yes                 |
| **GET /invoices**              | Yes (all or with `?user_id=` filter)    | Yes (own only)      |
| **Contacts CRUD (/contacts…)** | Yes (all)                               | Yes (own only)      |
| **GET /login-history**         | Yes (filterable)                        | No                  |


---

## Security notes
- **Exercise requirement** says passwords arrive already MD5-hashed from the frontend. The API stores that hash as-is in `users.password_md5`.
- For real systems, **MD5 is insecure**. Use Argon2/bcrypt/scrypt and **HTTPS** end-to-end.
- Access tokens expire in `ACCESS_TOKEN_EXPIRES_MIN` (default 15 min).
- Refresh tokens valid for `REFRESH_TOKEN_EXPIRES_DAYS` (default 7 days). Endpoint: `POST /refresh-token`.

---

## Minimal cURL flow

### Register (self-registers as user)
```bash
curl -s -X POST http://127.0.0.1:5000/register \
	-H 'Content-Type: application/json' \
	-d '{"username":"johndoe","password_md5":"13b27e73be9e7348661087267dc31c12"}'
```
Response: `{ "access_token": "...", "refresh_token": "..." }`

### Login
```bash
curl -s -X POST http://127.0.0.1:5000/login \
	-H 'Content-Type: application/json' \
	-d '{"username":"johndoe","password_md5":"13b27e73be9e7348661087267dc31c12"}'
```

### Me
```bash
curl -s http://127.0.0.1:5000/me \
	-H 'Authorization: Bearer REPLACE_WITH_ACCESS_TOKEN'
```

### Create product (admin only)
```bash
curl -s -X POST http://127.0.0.1:5000/products \
	-H 'Authorization: Bearer ADMIN_ACCESS_TOKEN' \
	-H 'Content-Type: application/json' \
	-d '{"name":"Apple","price":0.35,"entry_date":"2025-08-30","quantity":200}'
```

### Purchase
```bash
curl -s -X POST http://127.0.0.1:5000/purchase \
	-H 'Authorization: Bearer USER_ACCESS_TOKEN' \
	-H 'Content-Type: application/json' \
	-d '{"items":[{"product_id":1,"quantity":3},{"product_id":2,"quantity":1}]}'
```

### Invoices
```bash
# user sees own
curl -s http://127.0.0.1:5000/invoices -H 'Authorization: Bearer USER_ACCESS_TOKEN'

# admin sees all or by user
curl -s 'http://127.0.0.1:5000/invoices?user_id=1' -H 'Authorization: Bearer ADMIN_ACCESS_TOKEN'
```

### Refresh token
```bash
curl -s -X POST http://127.0.0.1:5000/refresh-token \
	-H 'Content-Type: application/json' \
	-d '{"refresh_token":"REPLACE_WITH_REFRESH_TOKEN"}'
```
