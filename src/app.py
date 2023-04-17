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
from models import db, User, FavoritePeople, People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    users=list(map(lambda item: item.serialize(), users))
    print(users)
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(users), 200

@app.route('/register', methods=['POST'])
def register_user():
    body=request.get_json()
    email=body["email"]
    name=body["name"]
    password=body["password"]
    is_active=body["is_active"]
    if body is None:
        raise APIException("You nned to specify the request body as json object", status_code=400)
    if "email" not in body:
        raise APIException("specify the email", status_code=400)
    new_user=User(email=email, name=name, password=password, is_active=is_active)
    db.session.add(new_user)
    db.session.commit()
      
    return jsonify({"mensaje":"Usuario creado"}), 201

@app.route('/user/<int:id>', methods=['GET'])
def get_specify_user(id):
    user = User.query.get(id)

    return jsonify(user.serialize()), 200

@app.route('/get_user', methods=['POST'])
def get_specify_user2():
    body = request.get_json()
    id = body["id"]
    user = User.query.get(id)
    return jsonify(user.serialize()), 200

@app.route('/get_user', methods=['DELETE'])
def delete_specify_user():
    body = request.get_json()
    id = body["id"]
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify("Usuario eliminado"), 200

@app.route('/get_user', methods=['PUT'])
def edit_specify_user():
    body = request.get_json()
    id = body["id"]
    name=body["name"]
    user = User.query.get(id)
    user.name=name

    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/add-favorite/people', methods=['POST'])
def add_favorite_people():
    body = request.get_json()
    user_id = body["user_id"]
    people_id = body["people_id"]

    character = People.query.get(people.id)
    if not character:
        raise APIException("personaje no encontrado", status_code=404)

    user = user.query.get(user_id).first()
    if not user:
        raise APIException("usuario no encontrado", status_code=404)

    fav_exist = FavoritePeople.query.filter_by(user_id=user.id, people_id=character.id).first() is not None
    if not fav_exist:
        raise APIException("El usuario ya lo tiene agregado a favoritos", status_code=404)
    
    favorite_people = FavoritePeople(user_id=user.id, people_id=character.id)
    db.session.add(favorite_people)
    db.session.commit()

@app.route('/favorites', methods=['POST'])
def list_Favorites():
    body = request.get_json()
    user_id = body["user_id"]
    if not user_id:
        raise APIException("Faltan datos", status_code=404)

    user= User.query.get(user_id)
    if not user:
        raise APIException("usuario no encontrado", status_code=404)

    user_favorites = FavoritePeople.query.filter_by(user_id=user.id).all()
    user_favorites_final = list(map(lambda item: item.serialize(), user_favorites))

    return jsonify(user_favorites_final), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
