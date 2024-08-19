from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Definir las tablas intermedias primero
user_favorites_planets = db.Table('user_favorites_planets',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
)

user_favorites_people = db.Table('user_favorites_people',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
)

people_films = db.Table('people_films',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

species_people = db.Table('species_people',
    db.Column('species_id', db.Integer, db.ForeignKey('species.id'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
)

people_starships = db.Table('people_starships',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('starship_id', db.Integer, db.ForeignKey('starship.id'), primary_key=True)
)

people_vehicles = db.Table('people_vehicles',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True)
)

planets_people = db.Table('planets_people',
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
)

species_films = db.Table('species_films',
    db.Column('species_id', db.Integer, db.ForeignKey('species.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

starships_films = db.Table('starships_films',
    db.Column('starship_id', db.Integer, db.ForeignKey('starship.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

vehicles_films = db.Table('vehicles_films',
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

planets_films = db.Table('planets_films',
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

# Definir los modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites_planets = db.relationship('Planet', secondary=user_favorites_planets)
    favorites_people = db.relationship('People', secondary=user_favorites_people)

    def __repr__(self):
        return f'<User {self.email}>'

class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    height = db.Column(db.String(50))
    mass = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    homeworld = db.Column(db.String(250))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    image = db.Column(db.String(250), nullable=True)

    films = db.relationship('Film', secondary=people_films)
    starships = db.relationship('Starship', secondary=people_starships)
    vehicles = db.relationship('Vehicle', secondary=people_vehicles)
    species = db.relationship('Species', secondary=species_people)
    planets = db.relationship('Planet', secondary=planets_people)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'eye_color': self.eye_color,
            'gender': self.gender,
            'hair_color': self.hair_color,
            'height': self.height,
            'mass': self.mass,
            'skin_color': self.skin_color,
            'homeworld': self.homeworld,
            'created': self.created,
            'edited': self.edited,
        }

class Film(db.Model):
    __tablename__ = 'film'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    episode_id = db.Column(db.Integer, nullable=False)
    opening_crawl = db.Column(db.String)
    director = db.Column(db.String(250))
    producer = db.Column(db.String(250))
    release_date = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)

    species = db.relationship('Species', secondary=species_films)
    starships = db.relationship('Starship', secondary=starships_films)
    vehicles = db.relationship('Vehicle', secondary=vehicles_films)
    planets = db.relationship('Planet', secondary=planets_films)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'episode_id': self.episode_id,
            'opening_crawl': self.opening_crawl,
            'director': self.director,
            'producer': self.producer,
            'release_date': self.release_date,
            'created': self.created,
            'edited': self.edited,
        }

class Starship(db.Model):
    __tablename__ = 'starship'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250))
    starship_class = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    cost_in_credits = db.Column(db.String(50))
    length = db.Column(db.String(50))
    crew = db.Column(db.String(50))
    passengers = db.Column(db.String(50))
    max_atmosphering_speed = db.Column(db.String(50))
    hyperdrive_rating = db.Column(db.String(50))
    MGLT = db.Column(db.String(50))
    cargo_capacity = db.Column(db.String(50))
    consumables = db.Column(db.String(50))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)

    films = db.relationship('Film', secondary=starships_films)
    pilots = db.relationship('People', secondary=people_starships)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'starship_class': self.starship_class,
            'manufacturer': self.manufacturer,
            'cost_in_credits': self.cost_in_credits,
            'length': self.length,
            'crew': self.crew,
            'passengers': self.passengers,
            'max_atmosphering_speed': self.max_atmosphering_speed,
            'hyperdrive_rating': self.hyperdrive_rating,
            'MGLT': self.MGLT,
            'cargo_capacity': self.cargo_capacity,
            'consumables': self.consumbales,
            'created': self.created,
            'edited': self.edited,
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250))
    vehicle_class = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    length = db.Column(db.String(50))
    cost_in_credits = db.Column(db.String(50))
    crew = db.Column(db.String(50))
    passengers = db.Column(db.String(50))
    max_atmosphering_speed = db.Column(db.String(50))
    cargo_capacity = db.Column(db.String(50))
    consumables = db.Column(db.String(50))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    image = db.Column(db.String(250), nullable=True)

    films = db.relationship('Film', secondary=vehicles_films)
    pilots = db.relationship('People', secondary=people_vehicles)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'vehicle_class': self.vehicle_class,
            'manufacturer': self.manufacturer,
            'length': self.length,
            'cost_in_credits': self.cost_in_credits,
            'crew': self.crew,
            'passengers': self.passengers,
            'max_atmosphering_speed': self.max_atmosphering_speed,
            'cargo_capacity': self.cargo_capacity,
            'consumables': self.consumables,
            'created': self.created,
            'edited': self.edited,
        }

class Species(db.Model):
    __tablename__ = 'species'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    classification = db.Column(db.String(250))
    designation = db.Column(db.String(250))
    average_height = db.Column(db.String(50))
    average_lifespan = db.Column(db.String(50))
    eye_colors = db.Column(db.String(250))
    hair_colors = db.Column(db.String(250))
    skin_colors = db.Column(db.String(250))
    language = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)

    people = db.relationship('People', secondary=species_people)
    films = db.relationship('Film', secondary=species_films)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'classification': self.classification,
            'designation': self.designation,
            'average_height': self.average_height,
            'average_lifespan': self.average_lifespan,
            'eye_colors': self.eye_colors,
            'hair_colors': self.hair_colors,
            'skin_colors': self.skin_colors,
            'language': self.language,
            'homeworld': self.homeworld,
            'created': self.created,
            'edited': self.edited,
        }

class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(50))
    rotation_period = db.Column(db.String(50))
    orbital_period = db.Column(db.String(50))
    gravity = db.Column(db.String(50))
    population = db.Column(db.String(50))
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.String(50))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    image = db.Column(db.String(250), nullable=True)

    residents = db.relationship('People', secondary=planets_people)
    films = db.relationship('Film', secondary=planets_films)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'diameter': self.diameter,
            'rotation_period': self.rotation_period,
            'orbital_period': self.orbital_period,
            'gravity': self.gravity,
            'population': self.population,
            'climate': self.climate,
            'terrain': self.terrain,
            'surface_water': self.surface_water,
            'created': self.created,
            'edited': self.edited,
        }