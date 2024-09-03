from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Color {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    diameter = db.Column(db.Float, nullable=False)
    rotation_period = db.Column(db.Float, nullable=False)
    orbital_period = db.Column(db.Float, nullable=False)
    gravity = db.Column(db.Float, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    surface_water = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Planet {self.name}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "surface_water": self.surface_water
        }

class Gender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Gender {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    homeworld = db.Column(db.Integer, db.ForeignKey("planet.id"))
    eye_color_id = db.Column(db.Integer, db.ForeignKey("color.id"))
    hair_color_id = db.Column(db.Integer, db.ForeignKey("color.id"))
    skin_color_id = db.Column(db.Integer, db.ForeignKey("color.id"))
    gender_id = db.Column(db.Integer, db.ForeignKey("gender.id"))
    name = db.Column(db.String, nullable=False)
    birth_year = db.Column(db.String)
    height = db.Column(db.Float, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Character {self.name}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "homeworld": self.homeworld,
            "eye_color_id": self.eye_color_id,
            "hair_color_id": self.hair_color_id,
            "skin_color_id": self.skin_color_id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender_id": self.gender_id,
            "height": self.height,
            "mass": self.mass
        }

class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    path = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Entity {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path
        }
