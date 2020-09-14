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
    Cooker.add_cooker(new_cooker)
    return  "success",200

@app.route('/cookers/<int:id>', methods=['GET'])
def handle_cooker(id):
    return jsonify(Cooker.get_cooker(id)), 200

@app.route('/cookers', methods=['GET'])
def handle_cookers():
    return jsonify(Cooker.get_cookers()), 200

@app.route('/cookers/<int:id>', methods=['PATCH', 'PUT'])
def handle_edit_Cooker(id): 
    cooker_edit= request.get_json()
    Cooker.update_cooker(id,cooker_edit)
    return "You have modificate cooker", 203

@app.route('/cookers/<int:id>', methods=['DELETE'])
def handle_delete_cooker(id):
    Cooker.delete_cooker(id) 
    return "You have delete cooker"

@app.route('/called', methods=['POST'])
def handle_new_called():
    new_called = request.get_json()
    Called.add_called(new_called)
    return "You creater new called", 201 

@app.route('/calleds', methods=['GET'])
def handle_all_called():
    print("You have recived all calleds") 
    return jsonify(Called.get_all_called()), 200

@app.route('/calleds/<int:id>', methods=['GET'])
def handle_called(id):
    print("You have recived one called") 
    return jsonify(Called.get_called(id)), 200

@app.route('/calleds/<int:id>', methods=['PATCH', 'PUT'])
def handle_edit_called(id):
    called_edit= request.get_json()
    Called.update_called(id,called_edit)
    return "You have modificate called, 203

@app.route('/calleds/<int:id>', methods=['DELETE'])
def handle_delete_order(id):
   Called.delete_called(id) 
    return "You have delete order", 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
