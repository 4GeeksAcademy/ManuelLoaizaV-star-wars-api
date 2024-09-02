"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import generate_sitemap, validate_color
from admin import setup_admin
from models import db, Character, Color, EntityType, Favorite, Gender, Planet, User

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

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

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

@app.route("/planets")
def fetch_planets():
    try:
        planets = Planet.query.all()
        return jsonify(list(map(lambda planet: planet.serialize(), planets))), 200
    except Exception as e:
        return jsonify({ "message": str(e) }), 500

@app.route("/planets/<int:planet_id>")
def fetch_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify({ "message": f"Planet with ID {planet_id} not found." }), 404
        return jsonify(planet.serialize()), 200
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
