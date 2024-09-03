import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import generate_sitemap, validate_character, validate_color, validate_gender, validate_planet
from admin import setup_admin
from models import db, Character, Color, Entity, Gender, Planet, User

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

class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv

@app.route("/populate")
def populate_db():
    try:
        manuel = User(
            name="Manuel",
            email="manuel@4geeks.com",
            hashed_password="GzY0J2NkXIzKNSz8gE6eNw==",
            is_active=True
        )
        astrid = User(
            name="Astrid",
            email="astrid@4geeks.com",
            hashed_password="6W4A/Rclf3zB4Wb1wopFWA==",
            is_active=True
        )
        frank = User(
            name="Frank",
            email="frank@4geeks.com",
            hashed_password="o1UZkTS9WDb1Baw7t6/Utg==",
            is_active=False
        )
        david = User(
            name="David",
            email="david@4geeks.com",
            hashed_password="JOSCvfkN5ilidJ/jBXC1oA==",
            is_active=True
        )
        db.session.add(manuel)
        db.session.add(frank)
        db.session.add(astrid)
        db.session.add(david)

        tatooine = Planet(
            name="Tatooine",
            rotation_period=23, 
            orbital_period=304, 
            diameter=10465,
            gravity=1,
            surface_water=1, 
            population=200000,
        )
        alderaan = Planet(
            name="Alderaan",
            rotation_period=24,
            orbital_period=364,
            diameter=12500,
            gravity=1,
            surface_water=40,
            population=2000000000,
        )
        db.session.add(tatooine)
        db.session.add(alderaan)

        blue = Color(name="blue")
        green = Color(name="green")
        black = Color(name="black")
        fair = Color(name="fair")
        blond = Color(name="blond")
        white = Color(name="white")
        yellow = Color(name="yellow")
        db.session.add(blue)
        db.session.add(black)
        db.session.add(green)
        db.session.add(fair)
        db.session.add(blond)
        db.session.add(white)
        db.session.add(yellow)

        male = Gender(name="Male")
        female = Gender(name="Female")
        unknown = Gender(name="Unknown")
        db.session.add(male)
        db.session.add(female)
        db.session.add(unknown)

        db.session.commit()

        luke = Character(
            name="Luke Skywalker",
            homeworld_id=1,
            height=172,
            mass=77,
            hair_color_id=5,
            skin_color_id=4,
            eye_color_id=1,
            birth_year="19BBY",
            gender_id=1
        )
        vader = Character(
            name="Darth Vader",
            homeworld_id=1,
            height=202,
            mass=136,
            skin_color_id=6,
            eye_color_id=7,
            birth_year="41.9BBY",
            gender_id=1
        )
        db.session.add(luke)
        db.session.add(vader)

        character = Entity(name="Character", path="people")
        planet = Entity(name="Planet", path="planets")
        vehicle = Entity(name="Vehicle", path="vehicles")
        starship = Entity(name="Starship", path="starships")
        db.session.add(character)
        db.session.add(planet)
        db.session.add(vehicle)
        db.session.add(starship)

        db.session.commit()
        return (""), 204
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/entities")
def fetch_entities():
    try:
        entities = Entity.query.all()
        return jsonify(list(map(lambda entity: entity.serialize(), entities))), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/entities/<int:entity_id>")
def fetch_entity_by_id(entity_id):
    try:
        entity = Entity.query.get(entity_id)
        if entity is None:
            return jsonify({ "message": f"Entity with ID {entity_id} not found." }), 404
        return jsonify(entity.serialize()), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/genders")
def fetch_genders():
    try:
        genders = Gender.query.all()
        return jsonify(list(map(lambda gender: gender.serialize(), genders))), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/genders/<int:gender_id>")
def fetch_gender_by_id(gender_id):
    try:
        gender = Gender.query.get(gender_id)
        if gender is None:
            return jsonify({ "message": f"Gender with ID {gender_id} not found." }), 404
        return jsonify(gender.serialize()), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/genders", methods=["POST"])
def create_gender():
    data = request.json
    is_valid, errors = validate_gender(data)
    if not is_valid:
        raise InvalidAPIUsage(
            message="Unprocessable Entity",
            status_code=422,
            payload=errors
        )
    try:
        new_gender = Gender(name=data["name"])
        db.session.add(new_gender)
        db.session.commit()
        return jsonify(new_gender.serialize()), 201
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/genders/<int:gender_id>", methods=["DELETE"])
def delete_gender(gender_id):
    try:
        gender = Gender.query.get(gender_id)
        if gender is not None:
            db.session.delete(gender)
            db.session.commit()
        return (""), 204
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/colors")
def fetch_colors():
    try:
        colors = Color.query.all()
        return jsonify(list(map(lambda color: color.serialize(), colors))), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/colors/<int:color_id>")
def fetch_color_by_id(color_id):
    try:
        color = Color.query.get(color_id)
        if color is None:
            return jsonify({ "message": f"Color with ID {color_id} not found." }), 404
        return jsonify(color.serialize()), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/colors", methods=["POST"])
def create_color():
    data = request.json
    is_valid, errors = validate_color(data)
    if not is_valid:
        raise InvalidAPIUsage(
            message="Unprocessable Entity",
            status_code=422,
            payload=errors
        )
    try:
        new_color = Color(name=data["name"])
        db.session.add(new_color)
        db.session.commit()
        return jsonify(new_color.serialize()), 201
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/colors/<int:color_id>", methods=["DELETE"])
def delete_color(color_id):
    try:
        color = Color.query.get(color_id)
        if color is not None:
            db.session.delete(color)
            db.session.commit()
        return (""), 204
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/people")
def fetch_characters():
    try:
        characters = Character.query.all()
        return jsonify(list(map(lambda character: character.serialize(), characters))), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/people/<int:character_id>")
def fetch_character_by_id(character_id):
    try:
        character = Character.query.get(character_id)
        if character is None:
            return jsonify({ "message": f"Character with ID {character_id} not found." }), 404
        return jsonify(character.serialize()), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/people", methods=["POST"])
def create_character():
    data = request.json
    is_valid, errors = validate_character(data)
    if not is_valid:
        raise InvalidAPIUsage(
            message="Unprocessable Entity",
            status_code=422,
            payload=errors
        )
    try:
        homeworld_id = data.get("homeworld_id")
        if homeworld_id is not None:
            homeworld = Planet.query.get(homeworld_id)
            if homeworld is None:
                return jsonify({ "message": f"Planet with ID {homeworld_id} not found." }), 404

        eye_color_id = data.get("eye_color_id")
        if eye_color_id is not None:
            eye_color = Color.query.get(eye_color_id)
            if eye_color is None:
                return jsonify({ "message": f"Color with ID {eye_color_id} not found." }), 404

        hair_color_id = data.get("hair_color_id")
        if hair_color_id is not None:
            hair_color = Color.query.get(hair_color_id)
            if hair_color is None:
                return jsonify({ "message": f"Color with ID {hair_color_id} not found." }), 404
        
        skin_color_id=data.get("skin_color_id")
        if skin_color_id is not None:
            skin_color = Color.query.get(skin_color_id)
            if skin_color is None:
                return jsonify({ "message": f"Color with ID {skin_color_id} not found." }), 404
        
        gender_id = data.get("gender_id")
        if gender_id is not None:
            gender = Gender.query.get(gender_id)
            if gender is None:
                return jsonify({ "message": f"Gender with ID {gender_id} not found." }), 404

        new_character = Character(
            homeworld_id=homeworld_id,
            eye_color_id=eye_color_id,
            hair_color_id=hair_color_id,
            skin_color_id=skin_color_id,
            gender_id=gender_id,
            name=data["name"],
            birth_year=data.get("birth_year"),
            height=data["height"],
            mass=data["mass"]
        )
        db.session.add(new_character)
        db.session.commit()
        return jsonify(new_character.serialize()), 201
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/people/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    try:
        character = Character.query.get(character_id)
        if character is not None:
            db.session.delete(character)
            db.session.commit()
        return (""), 204
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/planets")
def fetch_planets():
    try:
        planets = Planet.query.all()
        return jsonify(list(map(lambda planet: planet.serialize(), planets))), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/planets/<int:planet_id>")
def fetch_planet_by_id(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify({ "message": f"Planet with ID {planet_id} not found." }), 404
        return jsonify(planet.serialize()), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/planets", methods=["POST"])
def create_planet():
    data = request.json
    is_valid, errors = validate_planet(data)
    if not is_valid:
        raise InvalidAPIUsage(
            message="Unprocessable Entity",
            status_code=422,
            payload=errors
        )
    try:
        new_planet = Planet(
            name=data["name"],
            diameter=data["diameter"],
            rotation_period=data["rotation_period"],
            orbital_period=data["orbital_period"],
            gravity=data["gravity"],
            population=data["population"],
            surface_water=data["surface_water"]
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 201
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is not None:
            db.session.delete(planet)
            db.session.commit()
        return (""), 204
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/users")
def fetch_users():
    try:
        users = User.query.all()
        return jsonify(list(map(lambda user: user.serialize(), users))), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/users/<int:user_id>")
def fetch_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({ "message": f"User with ID {user_id} not found." }), 404
        return jsonify(user.serialize()), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
