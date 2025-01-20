from lib.db.db_connection import get_flask_database_connection
from flask import current_app, g
# from quart import current_app, g
from lib.repositories.users_repo import UserRepository
from lib.repositories.sightings_repo import SightingRepository
from lib.repositories.recipes_repo import RecipeRepository
from lib.repositories.ingredients_repo import IngredientRepository
from lib.repositories.steps_repo import StepRepository


async def connect_to_user_repository():
        # check for existence of user_repository in flask g (global) 
        if not hasattr(g, "user_repository"):
            # if global user_repository does't exist create a database connection...
            db_connection = await get_flask_database_connection(current_app)
            # ...then create user_repository globally using the database connection.
            g.user_repository = UserRepository(db_connection)

        # METHOD 2 (not as useful as connection not global)
        # db_connection = await get_flask_database_connection(current_app)
        # user_repository = UserRepository(db_connection)
        # users = await user_repository.get_all_users()

async def connect_to_sightings_repository():
        if not hasattr(g, "sightings_repository"):
            db_connection = await get_flask_database_connection(current_app)
            g.sightings_repository = SightingRepository(db_connection)

async def connect_to_recipes_repository():
        if not hasattr(g, "recipes_repository"):
            db_connection = await get_flask_database_connection(current_app)
            g.recipes_repository = RecipeRepository(db_connection)

async def connect_to_ingredients_repository():
        if not hasattr(g, "ingredients_repository"):
            db_connection = await get_flask_database_connection(current_app)
            g.ingredients_repository = IngredientRepository(db_connection)

async def connect_to_steps_repository():
        if not hasattr(g, "steps_repository"):
            db_connection = await get_flask_database_connection(current_app)
            g.steps_repository = StepRepository(db_connection)

async def connect_to_ratings_repository():
        if not hasattr(g, "ratings_repository"):
            db_connection = await get_flask_database_connection(current_app)
            g.ratings_repository = StepRepository(db_connection)