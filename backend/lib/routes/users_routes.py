import os
from flask import Blueprint, jsonify, g, request, redirect, send_from_directory
from lib.models.users import User
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)
from lib.repositories.repo_factory import connect_to_user_repository #import custom connect_to_user_repository() function from repo_factory.py file

#Create a Blueprint for a user-related route
user_routes = Blueprint('user_routes', __name__)

# create user route --> signup
@user_routes.route('/users/signup', methods=['POST'])
async def create_user():
    try:
        request_data = request.get_json()
        await connect_to_user_repository()
        
        username = request_data["username"]
        email = request_data["email"]
        password = request_data["password"]
        
        if not username or not email or not password:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        existing_user = await g.user_repository.get_single_user_by_email(email)
        if existing_user:
            return jsonify({"success": False, "message": "Email already registered"}), 409

        user = User(None, username, email, password)
        
        await g.user_repository.create_user(user)
        return jsonify({"success": True, "message": "Signup successful"}), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"gerror": str(e),}), 500
    
# login route
@user_routes.route('/users/login', methods=['POST'])
async def login_user():
    try: 
        request_data = request.get_json()
        email = request_data['email']
        password = request_data['password']
        hashed_password = request_data['password']
        payload = {"email": email, "password": password}
        await connect_to_user_repository()
        user_validated = await g.user_repository.validate_user(payload)
        if user_validated == True:
            user = await g.user_repository.get_single_user_by_email(email)
            # filter relevant data (i.e. NOT PASSWORD)
            user_dict = {"id": user.id, "username": user.username, "email": user.email, "profile_picture": user.profile_picture}
            # generate user token
            token = create_access_token(identity=user_dict)
            return jsonify({"success": True, "message": "Login successful", "token": token}), 200
        else:
            return jsonify({"success": False, "message": "Incorrect username or password"}), 401
    
    except Exception as e:
        raise Exception(e)
        print(f"Error: {e}")
        return jsonify({"error": str(e),}), 500

# ROUTES BELOW NEED MORE WORK/CONSIDERATION

# get all users route
@user_routes.route('/users', methods=['GET'])
# define route handler function below route decorator
async def get_users():
    #try/execpt block for error handling
    try:
        # connect to global user repository using connect_to_user_repository() function
        await connect_to_user_repository()
        users = await g.user_repository.get_all_users()
        # turn User objects into JSON
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        print(f"Error: {e}")
        #if error getting users return 500 staus with error message (JSON format)
        return jsonify({"error": str(e),}), 500
    
# Add additional routes below

# get user by id
@user_routes.route('/users/<id>', methods=['GET'])
async def get_user_by_id(id):
    try:
        await connect_to_user_repository()
        user = await g.user_repository.get_single_user_by_id(id)
        if user:
            return jsonify(user.to_dict())
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e),}), 500

# get user by username
@user_routes.route('/users/<username>', methods=['GET'])
async def get_user_by_username(username):
    try:
        await connect_to_user_repository()
        user = await g.user_repository.get_single_user_by_username(username)
        if user:
            return jsonify(user.to_dict())
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e),}), 500

# change profile pic
@user_routes.route('/files/upload', methods=['POST'])
async def change_profile_pic():
    try:
        await connect_to_user_repository()
        uploaded_file = request.files.get('file')
        user_id = request.form.get('user_id')
        print(uploaded_file)
        if not uploaded_file:
            return jsonify({"error": "No file provided"}), 400
        if uploaded_file.filename != "":
            filepath = os.path.join("uploads/profile", uploaded_file.filename)
            uploaded_file.save(filepath)
            image = uploaded_file.filename
            await g.user_repository.update_user_picture(filepath, int(user_id))
            return jsonify({"success": "check user_repo.update_user_picture if problems arise", "filepath": filepath}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e),}), 500


# load user profile pic
@user_routes.route('/uploads/<path:filename>')
def serve_file(filename):
    return send_from_directory('uploads', filename)

