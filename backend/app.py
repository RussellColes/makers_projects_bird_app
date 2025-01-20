import os
from flask import Flask
# from quart import Quart
from flask_cors import CORS
from lib.routes.users_routes import user_routes #import all user routes 
from lib.routes.bird_sightings_routes import sightings_routes
from lib.routes.RecipeServices_routes import RecipeServices_routes #import all RecipeServices routes 
from dotenv import load_dotenv
import os
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
SECRET_KEY = os.getenv("SECRET_KEY")


# Create a new Flask app
app = Flask(__name__)
CORS(app)

# JWT Stuff
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# register route blueprints 
app.register_blueprint(user_routes)
app.register_blueprint(sightings_routes)
app.register_blueprint(RecipeServices_routes)

    #OLD CODE FOR Flask
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 8000)))

    # new code for Quart with hypercorn
# print(Quart(__name__))
# print("Am I running?")
# if __name__ == '__main__':
#     print("I'm inside")
#     import hypercorn.asyncio
#     hypercorn.asyncio.serve(app, config={"bind": f"0.0.0.0:{os.environ.get('PORT', 8000)}"})
# print("I am running")

