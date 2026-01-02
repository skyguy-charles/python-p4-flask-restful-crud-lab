from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Plant Store API</h1>'

# GET all plants
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    plants_list = [plant.to_dict() for plant in plants]
    return jsonify(plants_list), 200

# GET one plant by ID
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.filter_by(id=id).first()
    if plant:
        return jsonify(plant.to_dict()), 200
    return jsonify({"error": "Plant not found"}), 404

# POST create a new plant
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    new_plant = Plant(
        name=data.get('name'),
        image=data.get('image'),
        price=data.get('price'),
        is_in_stock=data.get('is_in_stock', True)
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.to_dict()), 201

# PATCH update a plant
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.filter_by(id=id).first()
    
    if not plant:
        return jsonify({"error": "Plant not found"}), 404
    
    data = request.get_json()
    
    # Update only the fields that are provided
    for key in data:
        setattr(plant, key, data[key])
    
    db.session.commit()
    
    return jsonify(plant.to_dict()), 200

# DELETE a plant
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.filter_by(id=id).first()
    
    if not plant:
        return jsonify({"error": "Plant not found"}), 404
    
    db.session.delete(plant)
    db.session.commit()
    
    # Return empty response with 204 status code
    return '', 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)

























































































