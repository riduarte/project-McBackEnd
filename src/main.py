"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Cooker, Order
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/cooker', methods=['POST'])
def handle_new_cooker():
    new_cooker = request.get_json()
    Cooker.addCooker(new_cooker)
    return "You creater new cooker", 200 

@app.route('/cookers/<int:id>', methods=['GET'])
def handle_cooker(id):
    print("You have recived one cooker") 
    return jsonify(Cooker.getUser(id)), 200

@app.route('/cookers', methods=['GET'])
def handle_cookers():
    print("You have recived all cookers") 
    return jsonify(Cooker.getUsers()), 200

@app.route('/cookers/<int:id>', methods=['DELETE'])
def handle_delete_cooker(id):
    Cooker.deleteCooker(id) 
    return "You have delete cooker"

@app.route('/order', methods=['POST'])
def handle_new_order():
    new_order = request.get_json()
    Order.addOrder(new_order)
    return "You creater new order", 200 

@app.route('/orders', methods=['GET'])
def handle_orders():
    print("You have recived all orders") 
    return jsonify(Order.getOrders()), 200

@app.route('/orders/<int:id>', methods=['GET'])
def handle_order(id):
    print("You have recived one cooker") 
    return jsonify(Order.getOrder(id)), 200

@app.route('/orders/<int:id>', methods=['DELETE'])
def handle_delete_order(id):
    Order.deleteOrder(id) 
    return "You have delete order"

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
