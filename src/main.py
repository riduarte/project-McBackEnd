import os
import json

#import requests
from flask import Flask, redirect, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient

from admin import setup_admin
from models import db, User, UserOAuth
from utils import APIException, generate_sitemap

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

#from models import Person

app = Flask(__name__)

app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

#--------------------------------------------------------------------
# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return UserOAuth.get(user_id)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

#---------------------------------------------------------------------------



@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


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

@app.route('/cooker', methods=['POST'])
def handle_new_cooker():
    cooker = Cooker()
    new_cooker = request.get_json()
    validation = validation_global_cooker(new_cooker)
    if validation == True:
        cooker.add_cooker(new_cooker)
        return  "Success email",200
    else:
        return "Error syntaxis",406
  
@app.route('/cookers/<int:id>', methods=['GET'])
def handle_cooker(id):
    return jsonify(Cooker.get_user(id)), 200

@app.route('/cookers', methods=['GET'])
def handle_cookers():
    return jsonify(Cooker.get_users())

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
    print("You have recived one called") 
    return jsonify(Called.get_called(id)), 200

@app.route('/calleds/<int:id>', methods=['PATCH', 'PUT'])
def handle_edit_called(id):
    called_edit = request.get_json()
    return Called.set_called(id,called_edit)

@app.route('/calleds/<int:id>', methods=['DELETE'])
def handle_delete_called(id):
    deleted_called = Called.delete_called(id) 
    return deleted_called

#------------------------------------------------------------------------------------------------
@app.route("/login")
def login():
    #return request.base_url, 200
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url.replace('http://', 'https://') + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url.replace('http://', 'https://'),
        redirect_url=request.base_url.replace('http://', 'https://') ,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = UserOAuth(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not UserOAuth.get(unique_id):
        UserOAuth.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("sitemap").replace('http://', 'https://'))

#---------------------------------------------------------------------------------------------------



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

