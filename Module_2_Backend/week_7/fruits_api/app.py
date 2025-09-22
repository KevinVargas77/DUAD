from flask import Flask
from config import settings
from db import init_db

from auth_routes import bp as auth_bp
from product_routes import bp as products_bp
from purchase_routes import bp as purchase_bp
from invoice_routes import bp as invoices_bp
from contacts_routes import bp as contacts_bp
from admin_routes import bp as admin_bp

app = Flask("fruits-api")

@app.get("/liveness")
def liveness():
    return {"status": "ok"}

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(invoices_bp)
app.register_blueprint(contacts_bp)
app.register_blueprint(admin_bp)

# Initialize database
init_db()
print("Fruits API starting...")

# Entry point for the Fruits API
if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=True)
