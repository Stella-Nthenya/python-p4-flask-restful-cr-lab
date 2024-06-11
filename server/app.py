#!/usr/bin/env python3

from flask import Flask, jsonify, request, abort
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
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        data = request.get_json()
        if not data or not 'name' in data or not 'image' in data or not 'price' in data:
            abort(400, description="Missing data in request body")
        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant is None:
            abort(404, description="Plant not found")
        return jsonify(plant.to_dict())

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
