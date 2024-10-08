from datetime import timedelta

from flask import Blueprint, request, jsonify

from models.user import User, user_schema, users_schema,  UserSchema
from models.roles import Role
from init import bcrypt, db
from utils import admin_required

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

# Define a blueprint for authentication-related routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Registering a user route
@auth_bp.route('/register', methods=['POST'])
def register_user():
    """
    Registers a new user in the system.

    Expects a JSON request body with 'username', 'email', and 'password'.
    Automatically assigns the user 'Author' and 'Reader' roles.
    Returns a success message, the registered user's data, and a JWT token on successful registration.
    
    Returns:
        - 201 on success with user data and token.
        - 409 if the email is already registered.
        - 400 if there are database constraint violations (e.g., unique or not-null violations).
        - 500 for any other server errors.
    """
    try:
        body_data = request.get_json()
        username = body_data.get('username')
        email = body_data.get('email')
        password = body_data.get('password')

        # Check if user already exists
        stmt = select(User).where(User.email == email)
        user = db.session.execute(stmt).scalar_one_or_none()
        if user:
            return jsonify({'message': 'Email already registered'}), 409
        
        # Create a new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        # Assign 'Author' and 'Reader' roles to the new user
        author_role = db.session.execute(select(Role).where(Role.role_name == 'Author')).scalar_one()
        reader_role = db.session.execute(select(Role).where(Role.role_name == 'Reader')).scalar_one()
        new_user.roles.append(author_role)
        new_user.roles.append(reader_role)

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Serialise the new user
        result = user_schema.dump(new_user)

        # Generate a JWT token for the new user
        access_token = create_access_token(identity=new_user.user_id, expires_delta=timedelta(days=1))

        return jsonify({'message': 'User registered successfully!', 'user': result, 'access_token': access_token}), 201
    
    except IntegrityError as err:
        db.session.rollback()
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique violation
            return {"error": "Email address must be unique"}, 400
        
    except Exception as e:
        return {"error": str(e)}, 500
    
# User login route
@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Authenticates a user and provides a JWT token if the credentials are valid.

    Expects a JSON request body with 'email' and 'password'.
    Returns a JWT token on successful login.

    Returns:
        - 200 on successful login with JWT token.
        - 400 if the email or password is not provided.
        - 401 if the credentials are incorrect.
        - 500 for any other server errors.
    """
    try:
        # Get the data from the body of the request
        body_data = request.get_json()

        # Make sure the request contains email and password
        if not body_data or not body_data.get("email") or not body_data.get("password"):
            return jsonify({'message': 'Email and password are required.'}), 400

        # Find the user in the database with thier email
        stmt = db.select(User).filter_by(email=body_data.get("email"))
        user = db.session.scalar(stmt)

        # If the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password_hash, body_data.get("password")):
            # Create the JWT
            access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=1))
            # Responce
            return jsonify({
                'message': 'User login successfully!', 
                'access_token': access_token
            }), 200
        # If login fails, return an error message
        else:
            return jsonify({'message': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """
    Retrieves a list of all registered users.

    Requires admin privileges and a valid JWT token.

    Returns:
        - 200 on success with a list of all users.
    """
    try:
        # Use session.execute with the select() construct
        stmt = select(User)
        users = db.session.execute(stmt).scalars().all()
        
        # Serialise the list of users
        result = users_schema.dump(users)
        return jsonify(result), 200
    
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Updating a user 
@auth_bp.route('/users', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user():
    """
    Updates the authenticated user's information.

    Expects a JSON request body with fields like 'username', 'email', 'old_password', and 'new_password'.
    If 'email' is provided, it must be unique.
    If updating the password, 'old_password' is required for validation.

    Returns:
        - 200 on successful update with the updated user data.
        - 400 for validation errors (e.g., missing old password for password update).
        - 403 if the old password is incorrect.
        - 404 if the user is not found.
        - 409 if the new email is already in use by another user.
        - 500 for any other server errors.
    """
    try:
        # Get the user id from the JWT token
        user_id = get_jwt_identity()
        # Get the user from the database
        stmt = select(User).where(User.user_id == user_id)
        user = db.session.execute(stmt).scalar_one_or_none()

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get the data from the body of the request
        body_data = UserSchema().load(request.get_json(), partial=True)

        # Update the users fields if provided
        if "username" in body_data:
            user.username = body_data["username"]

        # Check and update the user's email if provided
        if "email" in body_data:
            # Check the email is unique
            email_check = db.session.execute(select(User).where(User.email == body_data["email"])).scalar_one_or_none()
            if email_check and email_check.user_id != user_id:
                return jsonify({"errer": "Email already in use"}), 409
            user.email = body_data["email"]

         # Check if the user is trying to update the password
        if "new_password" in body_data:
            if "old_password" not in body_data:
                return jsonify({"error": "Old password is required to update the password"}), 400
            # Check if old password is correct
            if not user.check_password(body_data["old_password"]):
                return jsonify({"error": "Incorrect current password"}), 403
            
            # Update to the new password
            user.set_password(body_data["new_password"])
            
        # Save updates to the db
        db.session.commit()

        # Return the updated user data
        result = UserSchema().dump(user)
        return jsonify({"message": "User updated successfully", "user": result}), 200
     
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Deleting a user
@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    """
    Deletes a user from the system.

    The route allows users to delete their own account or, with the correct permissions, to delete other users.
    
    Permissions:
        - A user can delete their own account.
        - Admins can delete regular users.
        - Super Admins can delete Admins and Super Admins.
    
    Args:
        user_id (int): The ID of the user to be deleted (passed as a URL parameter).
    
    Returns:
        - 200 on successful deletion with a relevant message.
        - 403 if the user does not have permission to delete the specified user.
        - 404 if the current user or the target user does not exist.
        - 500 for any other server errors.
    """
    try:
        # Get the user from the JWT token
        current_user_id = get_jwt_identity()
        # Get the user from the DB
        stmt = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt).scalar_one_or_none()

        if not current_user:
            return jsonify({"error": "Current user not found"}), 404
        
        # Get the user to be deleted from the DB
        stmt = select(User).where(User.user_id == user_id)
        user_to_be_deleted = db.session.execute(stmt).scalar_one_or_none()

        if not user_to_be_deleted:
            return jsonify({"error": "User to be deleted not found"}), 404
        
        # To check if the current user is trying to delete thier own account
        if current_user_id == user_id:
            # User can delete thier own account
            db.session.delete(user_to_be_deleted)
            db.session.commit()
            return jsonify({"message": "Your account has been deleted"}), 200
        
        # Role checks
        # If the user to be deleted is admin
        if user_to_be_deleted.has_role("Admin"):
            if current_user.has_role("Super Admin"):
                # A super admin can delete an admin
                db.session.delete(user_to_be_deleted)
                db.session.commit()
                return jsonify({"message": f"Admin {user_to_be_deleted.username} has been deleted"}), 200
            else:
                # If they are not a super admin do not allow
                return jsonify({"error": "Only a Super Admin can delete an Admin"}), 403
            
        # If the user to be deleted is super admin
        if user_to_be_deleted.has_role("Super Admin"):
            if current_user.has_role("Super Admin"):
                # A super admin can delete a super admin
                db.session.delete(user_to_be_deleted)
                db.session.commit()
                return jsonify({"message": f"Super Admin {user_to_be_deleted.username} has been deleted"}), 200
            else:
                # If they are not a super admin do not allow
                return jsonify({"error": "Only a Super Admin can delete another Super Admin"}), 403
            
        # General user deletion
        if current_user.has_role("Admin") or current_user.has_role("Super Admin"):
            # Admin or super admin can delete regular users
            db.session.delete(user_to_be_deleted)
            db.session.commit()
            return jsonify({"message": f"User {user_to_be_deleted.username} has been deleted"}, 200)
        
        # If none of these conditions are met 
        return jsonify({"message": "You do not have permission to delete this user"}), 403
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500