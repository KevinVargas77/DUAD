from flask import Flask
from flask import jsonify, Blueprint, request

from auth import auth_bp
from users import users_bp
from products import products_bp
from shopping_carts import shopping_carts_bp
from checkout import checkout_bp
from payments import payments_bp

app = Flask(__name__)


app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(shopping_carts_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(payments_bp)

if __name__ == "__main__":
    app.run(debug=True)

