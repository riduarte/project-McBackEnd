import os
import bcrypt
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, validation_global_cooker
from admin import setup_admin
from models import db, Cooker, Called, Enterprise
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('nickname', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    cooker = Cooker.get_cooker_login(username, password)
    if cooker == None :
        return jsonify({"msg": "Bad username or password"}), 401
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token, cooker=cooker.serialize()), 200

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/enterprise', methods=['POST'])
def handle_new_enterprise():
    enterprise = Enterprise()
    new_enterprise = request.get_json()
    validation = validation_global_cooker(new_enterprise)
    check_new_username = request.json.get('nickname',None)
    check_new_password = request.json.get('password',None)
    if not check_new_username:
        return 'Missing username', 400
    if not check_new_password:
        return 'Missing password', 400
    if validation == True:
        enterprise.add_enterprise(new_enterprise)
        return  "Success email",200
    else:
        return "Error syntaxis",406

@app.route('/enterprises', methods=['GET'])
def handle_enterprises():
    return jsonify(Enterprise.get_enterprises())

@app.route('/cooker', methods=['POST'])
def handle_new_cooker():
    cooker = Cooker()
    new_cooker = request.get_json()
    validation = validation_global_cooker(new_cooker)
    check_new_username = request.json.get('nickname',None)
    check_new_password = request.json.get('password',None)
    if not check_new_username:
        return 'Missing username', 400
    if not check_new_password:
        return 'Missing password', 400
    if validation == True:
        cooker.add_cooker(new_cooker)
        return  "Success email",200
    else:
        return "Error syntaxis",406

@app.route('/cookers/<int:id>', methods=['GET'])
def handle_cooker(id):
    return jsonify(Cooker.get_cooker(id)), 200

@app.route('/cookers', methods=['GET'])
def handle_cookers():
    return jsonify(Cooker.get_cookers())

@app.route('/cookers/<int:id>', methods=['PATCH', 'PUT'])
def handle_edit_Cooker(id): 
    cooker_edit= request.get_json()
    return Cooker.set_user(id,cooker_edit)

@app.route('/cookers/<int:id>', methods=['DELETE'])
def handle_delete_cooker(id):
    delete_cooker = Cooker.delete_cooker(id) 
    return delete_cooker

@app.route('/called', methods=['POST'])
def handle_new_called():
    called = Called()
    new_called = request.get_json()
    called.add_called(new_called)
    return "You creater new called", 201 

@app.route('/calleds', methods=['GET'])
def handle_all_called():
    return jsonify(Called.get_all_called()), 200

@app.route('/calleds/<int:id>', methods=['GET'])
def handle_called(id):
    return jsonify(Called.get_called(id)), 200

@app.route('/calleds/<int:id>', methods=['PATCH', 'PUT'])
def handle_edit_called(id):
    called_edit = request.get_json()
    return Called.update_called(id,called_edit)

@app.route('/calleds/<int:id>', methods=['DELETE'])
def handle_delete_called(id):
    deleted_called = Called.delete_called(id) 
    return deleted_called

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)