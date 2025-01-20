from flask import Blueprint, jsonify, g, request, send_from_directory
from lib.services.RecipeServices import RecipeService
import os
from lib.repositories.repo_factory import (
    connect_to_sightings_repository,
    connect_to_recipes_repository,
    connect_to_ingredients_repository,
    connect_to_steps_repository)

#Create a Blueprint for a user-related route
RecipeServices_routes = Blueprint('RecipeServices_routes', __name__)

#POST a bird sighting (and generate a recipe) route
@RecipeServices_routes.route('/bird_sighting', methods=["POST"])
async def post_bird_sighting():
    try:
        await connect_to_sightings_repository()
        await connect_to_recipes_repository()
        await connect_to_ingredients_repository()
        await connect_to_steps_repository()

        # Parse incoming formData

        bird_name = request.form.get('birdName')
        print(bird_name)
        location = request.form.get('location')
        user_id = int(request.form.get('user_id'))
        uploaded_file = request.files.get('file')
        print(uploaded_file)

        if not uploaded_file:
            return jsonify({"error": "No file provided"}), 400

        if not bird_name or not user_id:
            return jsonify({"error": "bird_name and user_id are required"}), 400
        
        # Save file to backend/uploads and return filepath to add to create recipe and sighting
        if uploaded_file.filename != "":
            filepath = os.path.join("uploads", uploaded_file.filename)
            uploaded_file.save(filepath)
            image = uploaded_file.filename

            # Create an instance of RecipeService with your repositories and connection
            recipe_service = RecipeService(
                sightings_repo=g.sightings_repository,
                recipes_repo=g.recipes_repository,
                ingredients_repo=g.ingredients_repository,
                steps_repo=g.steps_repository,
                connection=g.flask_database_connection
            )

            # Call the async service method to create a recipe & bird sighting
            recipe_id = await recipe_service.create_recipe_from_bird_name(bird_name, user_id, location, image)
            print(recipe_id)
            if not recipe_id:
                return jsonify({"error": "Failed to create recipe"}), 500

            # If successful, return the newly created recipe_id
            return jsonify({"recipe_id": recipe_id, "image": image}), 201

    except Exception as e:
        # Catch and return any unhandled exceptions
        return jsonify({"error": str(e)}), 500
    
#Serve files (images) from the uploads directory
@RecipeServices_routes.route('/bird_uploads/<path:path>', methods=["GET"])
def get_uploads(path):
    return send_from_directory('uploads', path)


#GET a bird recipe according to its sighting_id and send to frontend in json format
@RecipeServices_routes.route('/bird_recipe/<int:sighting_id>', methods=["GET"])
async def get_bird_recipe_by_sighting_id(sighting_id):
    try:
        await connect_to_sightings_repository()
        await connect_to_recipes_repository()
        await connect_to_ingredients_repository()
        await connect_to_steps_repository()

        recipe_service = RecipeService(
            sightings_repo=g.sightings_repository,
            recipes_repo=g.recipes_repository,
            ingredients_repo=g.ingredients_repository,
            steps_repo=g.steps_repository,
            connection=g.flask_database_connection
        )

        # Note from Doug --> recipe is a dictionary object
        recipe = await recipe_service.get_recipe_from_sighting_id(sighting_id)

        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404

        return jsonify({"recipe": recipe}), 200

    except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    #GET all bird recipes according to its sighting_id and send to frontend in json format
