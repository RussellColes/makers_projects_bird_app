from flask import Blueprint, jsonify, g, request, redirect
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)
from lib.repositories.repo_factory import connect_to_ratings_repository
from lib.models.ratings import Rating

#Create a Blueprint for a sighting-related route
ratings_routes = Blueprint('ratings_routes', __name__)

@ratings_routes.route("/ratings/<recipe_id>", methods=["POST"])
async def post_recipe_rating(recipe_id):
    try:
        await connect_to_ratings_repository()
        request_data = request.get_json()
        rating_score = request_data["rating_score"]
        if not rating_score:
            return jsonify({"success": False, "message": "missing rating score"})
        new_rating = Rating(None, rating_score, recipe_id)
        await g.ratings_repository.create_rating(new_rating)
        return jsonify({"success": True, "message": "rating successfully added"})
    except Exception as e:
        print(f"error: {e}")
        return jsonify({"error": str(e)}), 500

        

