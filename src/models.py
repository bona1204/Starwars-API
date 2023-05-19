from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    name= db.Column(db.String(250), unique=False, nullable=False)
    favorite_people = db.relationship("FavoritePeople", backref="User", lazy=True)
    favorite_planet = db.relationship("FavoritePlanet", backref="User", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):   
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    mass = db.Column(db.String(120), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    favorite_people = db.relationship("FavoritePeople", backref="people", lazy=True)

    def serialize(self):   
        return {
            "id": self.id,
            "height": self.height,
            "name": self.name,
            "mass": self.mass,
            "hair_color": self.hair_color
          }

class FavoritePeople (db.Model):
    id=db.Column(db.Integer, primary_key=T rue)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    people_id= db.Column (db.Integer, db.ForeignKey("people.id"), nullable=False)

    def serialize(self):   
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "people_name": people.query.get(people_id).serialize()["name"],
            "user_name": User.query.get(self.user_id).serialize( )["name"],
            "user": User.query.get(self.User_id).serialize(),
            "people": People.query.get(self.people_id).serialize(),
          }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Diameter = db.Column(db.Integer, unique=False, nullable=False)
    Gravity = db.Column(db.String(120), unique=False, nullable=False)
    Terrain = db.Column(db.String(120), unique=False, nullable=False)
    Orbital_Period = db.Column(db.String, unique=False, nullable=False)
    favorite_planet = db.relationship("FavoritePlanet", backref="planet", lazy=True)

    def serialize(self):   
        return {
            "id": self.id,
            "Diameter": self.Diameter,
            "Gravity": self.Gravity,
            "Terrain": self.Terrain,
            "Orbital_Period": self.Orbital_Period
          }

class FavoritePlanet (db.Model):
    id=db.Column(db.Integer, primary_key=T rue)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id= db.Column (db.Integer, db.ForeignKey("planet.id"), nullable=False)

    def serialize(self):   
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet_name": planet.query.get(planet_id).serialize()["name"],
            "user_name": User.query.get(self.user_id).serialize( )["name"],
            "user": User.query.get(self.User_id).serialize(),
            "planet": Planet.query.get(self.planet_id).serialize(),
          }
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    model = db.Column(db.String(50), unique=False, nullable=False)
    manufacturer = db.Column(db.String(100), unique=False, nullable=False)
    cost_in_credits = db.Column(db.Integer, unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)
    favorite_vehicle = db.relationship('FavoriteVehicle', backref = 'vehicle', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            # do not serialize the password, its a security breach
        }
class FavoriteVehicle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id,
            "vehicle_name": planet.query.get(vehicle).serialize()["name"],
            "user_name": User.query.get(self.user_id).serialize( )["name"],
            "user": User.query.get(self.User_id).serialize(),
            "vehicle": Vehicle.query.get(self.vehicle_id).serialize()
        }