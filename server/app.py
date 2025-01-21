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

# Resource for `/plants`
class Plants(Resource):
    def get(self):
       plants =Plant.query.all()
        # plants_dict = [plant.to_dict() for plant in Plant.query.all()]
       return jsonify([plant.to_dict() for plant in  plants])
         


    def post(self):
        data = request.get_json()

        # Validate required fields
        required_fields = ["name", "image", "price"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return make_response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"}, 400
            )

        try:
            # Ensure fields are correctly provided
            new_plant = Plant(
                name=data["name"], 
                image=data["image"], 
                price=float(data["price"])  # Ensure price is a valid float
            )
            db.session.add(new_plant)
            db.session.commit()

            return make_response(new_plant.to_dict(), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 500)


# Resource for `/plants/<int:id>`
class PlantByID(Resource):
    def get(self, id):
        responce_dict = Plant.query.filter_by(id=id).first().to_dict()

        response = make_response(responce_dict, 200)

        return response




# Register resources
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
