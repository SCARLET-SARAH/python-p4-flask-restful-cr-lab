#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        try:
            plants = Plant.query.all()
            return jsonify([plant.to_dict() for plant in plants]), 200
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    def post(self):
        try:
            data = request.get_json()
            if 'name' not in data:
                return make_response(jsonify({'error': 'Name field is required'}), 400)
            plant = Plant(name=data['name'], image=data.get('image'), price=data.get('price'))
            db.session.add(plant)
            db.session.commit()
            return make_response(jsonify(plant.to_dict()), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

class PlantByID(Resource):
    def get(self, plant_id):
        try:
            plant = Plant.query.get(plant_id)
            if plant:
                return jsonify(plant.to_dict()), 200
            else:
                return make_response(jsonify({'error': 'Plant not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    def put(self, plant_id):
        try:
            plant = Plant.query.get(plant_id)
            if plant:
                data = request.get_json()
                if 'name' in data:
                    plant.name = data['name']
                if 'image' in data:
                    plant.image = data['image']
                if 'price' in data:
                    plant.price = data['price']
                db.session.commit()
                return jsonify(plant.to_dict()), 200
            else:
                return make_response(jsonify({'error': 'Plant not found'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    def delete(self, plant_id):
        try:
            plant = Plant.query.get(plant_id)
            if plant:
                db.session.delete(plant)
                db.session.commit()
                return make_response('', 204)
            else:
                return make_response(jsonify({'error': 'Plant not found'}), 404)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
