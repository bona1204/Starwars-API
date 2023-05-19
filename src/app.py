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
    if 'name' not in body:
        raise APIException('specify the name', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    new_user=User(email=email, name=name, password=password, is_active=is_active)
    db.session.add(new_user)
    db.session.commit()
      
    return jsonify({"mensaje":"Usuario creado"}), 201

@app.route('/get_user/<int:id>', methods=['GET'])
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

@app.route('/get_people/<int:id>', methods=['GET'])
def get_specify_people(id):
    people = People.query.get(id)

    return jsonify(people.serialize()), 200

@app.route('/get_people', methods=['POST'])
def get_specify_people2():
    body = request.get_json()
    id = body["id"]
    people = People.query.get(id)
    return jsonify(people.serialize()), 200

@app.route('/get_people', methods=['DELETE'])
def delete_specify_people():
    body = request.get_json()
    id = body["id"]
    people = People.query.get(id)
    db.session.delete(people)
    db.session.commit()
    return jsonify("Personaje eliminado"), 200

@app.route('/get_people', methods=['PUT'])
def edit_specify_people():
    body = request.get_json()
    id = body["id"]
    name=body["name"]
    people = People.query.get(id)
    people.name=name

    db.session.commit()
    return jsonify(people.serialize()), 200

@app.route('/get_planet/<int:id>', methods=['GET'])
def get_specify_planet(id):
    planet = Planet.query.get(id)

    return jsonify(planet.serialize()), 200

@app.route('/get_planet', methods=['POST'])
def get_specify_planet2():
    body = request.get_json()
    id = body["id"]
    planet = Planet.query.get(id)
    return jsonify(planet.serialize()), 200

@app.route('/get_planet', methods=['DELETE'])
def delete_specify_planet():
    body = request.get_json()
    id = body["id"]
    planet = Planet.query.get(id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify("Planeta eliminado"), 200

@app.route('/get_planet', methods=['PUT'])
def edit_specify_planet():
    body = request.get_json()
    id = body["id"]
    name=body["name"]
    planet = Planet.query.get(id)
    planet.name=name

    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route('/get_vehicle/<int:id>', methods=['GET'])
def get_specify_vehicle(id):
    vehicle = Vehicle.query.get(id)

    return jsonify(vehicle.serialize()), 200

@app.route('/get_vehicle', methods=['POST'])
def get_specify_planet2():
    body = request.get_json()
    id = body["id"]
    vehicle = Vehicle.query.get(id)
    return jsonify(vehicle.serialize()), 200

@app.route('/get_vehicle', methods=['DELETE'])
def delete_specify_vehicle():
    body = request.get_json()
    id = body["id"]
    vehicle = Vehicle.query.get(id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify("Vehiculo eliminado"), 200

@app.route('/get_vehicle', methods=['PUT'])
def edit_specify_vehicle():
    body = request.get_json()
    id = body["id"]
    name=body["name"]
    vehicle = Vehicle.query.get(id)
    vehicle.name=name

    db.session.commit()
    return jsonify(vehicle.serialize()), 200

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

     return jsonify(favorite_people.serialize()), 200

@app.route('/add-favorite/planet', methods=['POST'])
def add_favorite_people():
    body = request.get_json()
    user_id = body["user_id"]
    planet_id = body["people_id"]

    planet = Planet.query.get(planet.id)
    if not character:
        raise APIException("Planeta no encontrado", status_code=404)

    user = user.query.get(user_id).first()
    if not user:
        raise APIException("usuario no encontrado", status_code=404)

    fav_exist = FavoritePlanet.query.filter_by(user_id=user.id, planet_id=planet.id).first() is not None
    if not fav_exist:
        raise APIException("El usuario ya lo tiene agregado a favoritos", status_code=404)
    
    favorite_planet = FavoritePlanet(user_id=user.id, people_id=character.id)
    db.session.add(favorite_planet)
    db.session.commit()

     return jsonify(favorite_people.serialize()), 200


@app.route('/add-favorite/vehicle', methods=['POST'])
def add_favorite_vehicle():
    body = request.get_json()
    user_id = body['user_id']
    vehicle_id = body['vehicle_id']

    vehicle = Vehicle.query.get(vehicle_id) 
        raise APIException('Vehiculo no encontrado', status_code=404)
    
    user = User.query.get(user_id)
    if not user:
        raise APIException('usuario no encontrado', status_code=404)

    favorite_exist = FavoriteVehicle.query.filter_by(user_id = user.id, vehicle_id = vehicle.id).first() is not None
    
    if favorite_exist:
        raise APIException('El usuario ya lo tiene agregado a favoritos', status_code=404)

    favorite_vehicle = FavoriteVehicle(user_id = user.id, vehicle_id = vehicle.id)
    db.session.add(favorite_vehicle)
    db.session.commit()

    return jsonify(favorite_vehicle.serialize()), 200

@app.route('/favorites', methods=['POST'])
def list_Favorites():
    body = request.get_json()
    user_id = body["user_id"]
    if not user_id:
        raise APIException("Faltan datos", status_code=404)

    user= User.query.get(user_id)
    if not user:
        raise APIException("usuario no encontrado", status_code=404)

    user_favorites_people = FavoritePeople.query.filter_by(user_id=user.id).all()
    user_favorites_final_people = list(map(lambda item: item.serialize(), user_favorites_people))
    user_favorites_planet = FavoritePlanet.query.filter_by(user_id=user.id).all()
    user_favorites_final_planet = list(map(lambda item: item.serialize(), user_favorites_planet))
    user_favorites_vehicle = FavoriteVehicle.query.filter_by(user_id=user.id).all()
    user_favorites_final_vehicle = list(map(lambda item: item.serialize(), user_favorites_vehicle))

    return jsonify(user_favorites_final_people, user_favorites_final_planet, user_favorites_final_vehicle), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
