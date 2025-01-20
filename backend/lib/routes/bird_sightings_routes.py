from flask import Blueprint, jsonify, g, request, redirect
from lib.models.sightings import Sighting
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)
from lib.repositories.repo_factory import connect_to_sightings_repository

# NO NEED FOR POST ROUTES - CHECK RecipeServices.py LINE 56 "create_recipe_from_bird_name"

#Create a Blueprint for a sighting-related route
sightings_routes = Blueprint('sightings_routes', __name__)

# Get all sightings
@sightings_routes.route('/sightings', methods=['GET'])
async def get_sightings():
    try:
        await connect_to_sightings_repository()
        sightings = await g.sightings_repository.get_all_sightings()
        return jsonify([sighting.to_dict() for sighting in sightings])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e),}), 500
    
# Add additional routes below

# get sighting by sighting id
@sightings_routes.route('/sighting/<id>', methods=['GET'])
async def get_sighting_by_id(id):
    try:
        await connect_to_sightings_repository()
        sighting = await g.sightings_repository.get_sighting_by_id(id)
        if sighting:
            return jsonify(sighting.to_dict())
        else:
            return jsonify({"error": "Sighting not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e),}), 500

# get all sightings with a single user_id
@sightings_routes.route('/sightings/<user_id>', methods=['GET'])
async def get_sightings_by_user_id(user_id):
    user_id_int = int(user_id)
    print(user_id_int)
    try:
        await connect_to_sightings_repository()
        sightings = await g.sightings_repository.get_sightings_by_user_id(user_id_int)
        if sightings:
            return jsonify([sighting.to_dict() for sighting in sightings])
        else:
            return jsonify({"error": f"Sightings not found. user_id = {user_id_int}"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e),}), 500

