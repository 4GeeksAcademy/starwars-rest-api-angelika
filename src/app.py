"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from datetime import datetime
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Film, Starship, Vehicle, Species, Planet
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

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# Endpoints for People
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.to_dict() for person in people])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get_or_404(people_id)
    return jsonify(person.to_dict())

@app.route('/people', methods=['POST'])
def add_person():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({'error': 'Los datos deben ser un objeto JSON.'}), 400

        required_fields = ['name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido faltante: {field}'}), 400

        created = None
        edited = None
        try:
            if 'created' in data:
                created = datetime.strptime(data['created'], "%a, %d %b %Y %H:%M:%S GMT")
            if 'edited' in data:
                edited = datetime.strptime(data['edited'], "%a, %d %b %Y %H:%M:%S GMT")
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido'}), 400

        new_person = People(
            name=data.get('name'),
            birth_year=data.get('birth_year'),
            eye_color=data.get('eye_color'),
            hair_color=data.get('hair_color'),
            skin_color=data.get('skin_color'),
            height=data.get('height'),
            mass=data.get('mass'),
            gender=data.get('gender'),
            homeworld=data.get('homeworld'),
            created=created,
            edited=edited
        )

        db.session.add(new_person)
        db.session.commit()

        return jsonify(new_person.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoints for Planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.to_dict() for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify(planet.to_dict())

@app.route('/planets', methods=['POST'])
def add_planet():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({'error': 'Los datos deben ser un objeto JSON.'}), 400

        required_fields = ['name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido faltante: {field}'}), 400

        created = None
        edited = None
        try:
            if 'created' in data:
                created = datetime.strptime(data['created'], "%a, %d %b %Y %H:%M:%S GMT")
            if 'edited' in data:
                edited = datetime.strptime(data['edited'], "%a, %d %b %Y %H:%M:%S GMT")
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido'}), 400

        new_planet = Planet(
            name=data.get('name'),
            diameter=data.get('diameter'),
            rotation_period=data.get('rotation_period'),
            orbital_period=data.get('orbital_period'),
            gravity=data.get('gravity'),
            population=data.get('population'),
            climate=data.get('climate'),
            terrain=data.get('terrain'),
            surface_water=data.get('surface_water'),
            created=created,
            edited=edited,
            image=data.get('image')
        )

        db.session.add(new_planet)
        db.session.commit()

        return jsonify(new_planet.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoints for Vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.to_dict() for vehicle in vehicles])

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify(vehicle.to_dict())

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    try:
        data = request.get_json()

        created = None
        edited = None
        try:
            if 'created' in data:
                created = datetime.strptime(data['created'], "%a, %d %b %Y %H:%M:%S GMT")
            if 'edited' in data:
                edited = datetime.strptime(data['edited'], "%a, %d %b %Y %H:%M:%S GMT")
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido'}), 400
        
        new_vehicle = Vehicle(
            name=data.get('name'),
            model=data.get('model'),
            vehicle_class=data.get('vehicle_class'),
            manufacturer=data.get('manufacturer'),
            length=data.get('length'),
            cost_in_credits=data.get('cost_in_credits'),
            crew=data.get('crew'),
            passengers=data.get('passengers'),
            max_atmosphering_speed=data.get('max_atmosphering_speed'),
            cargo_capacity=data.get('cargo_capacity'),
            consumables=data.get('consumables'),
            created=created,
            edited=edited,
            image=data.get('image')
        )

        db.session.add(new_vehicle)
        db.session.commit()

        return jsonify({
            'id': new_vehicle.id,
            'name': new_vehicle.name,
            'model': new_vehicle.model,
            'vehicle_class': new_vehicle.vehicle_class,
            'manufacturer': new_vehicle.manufacturer,
            'length': new_vehicle.length,
            'cost_in_credits': new_vehicle.cost_in_credits,
            'crew': new_vehicle.crew,
            'passengers': new_vehicle.passengers,
            'max_atmosphering_speed': new_vehicle.max_atmosphering_speed,
            'cargo_capacity': new_vehicle.cargo_capacity,
            'consumables': new_vehicle.consumables,
            'created': new_vehicle.created.isoformat() if new_vehicle.created else None,
            'edited': new_vehicle.edited.isoformat() if new_vehicle.edited else None,
            'image': new_vehicle.image,
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Endpoints for Users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.email for user in users])

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    current_user_id = request.args.get('user_id', type=int, default=1)  # Placeholder
    user = User.query.get_or_404(current_user_id)
    favorite_planets = [planet.to_dict() for planet in user.favorites_planets]
    favorite_people = [person.to_dict() for person in user.favorites_people]
    return jsonify({
        'planets': favorite_planets,
        'people': favorite_people
    })

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user_id = request.args.get('user_id', type=int, default=1)  # Placeholder
    user = User.query.get_or_404(current_user_id)
    planet = Planet.query.get_or_404(planet_id)
    if planet not in user.favorites_planets:
        user.favorites_planets.append(planet)
        db.session.commit()
    return jsonify({'message': 'Favorite planet added!'})

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    current_user_id = request.args.get('user_id', type=int, default=1)  # Placeholder
    user = User.query.get_or_404(current_user_id)
    person = People.query.get_or_404(people_id)
    if person not in user.favorites_people:
        user.favorites_people.append(person)
        db.session.commit()
    return jsonify({'message': 'Favorite person added!'})

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    current_user_id = request.args.get('user_id', type=int, default=1)  # Placeholder
    user = User.query.get_or_404(current_user_id)
    planet = Planet.query.get_or_404(planet_id)
    if planet in user.favorites_planets:
        user.favorites_planets.remove(planet)
        db.session.commit()
    return jsonify({'message': 'Favorite planet removed!'})

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(people_id):
    current_user_id = request.args.get('user_id', type=int, default=1)  # Placeholder
    user = User.query.get_or_404(current_user_id)
    person = People.query.get_or_404(people_id)
    if person in user.favorites_people:
        user.favorites_people.remove(person)
        db.session.commit()
    return jsonify({'message': 'Favorite person removed!'})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
