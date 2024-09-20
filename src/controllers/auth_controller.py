from datetime import timedelta

from flask import Blueprint, request, jsonify

from models.user import User, user_schema, users_schema,  UserSchema
from init import bcrypt, db

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route('/register', methods=['POST'])
def register_user():
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
        db.session.add(new_user)
        db.session.commit()

        # Serialise the new user
        result = user_schema.dump(new_user)

        access_token = create_access_token(identity=new_user.id, expires_delta=timedelta(days=1))

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
    
@auth_bp.route("/login", methods=["POST"])
def login_user():
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
        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # Responce
        return jsonify({
            'message': 'User login successfully!', 
            'user': {'id': user.id, 'email': user.email},
            'access_token': access_token
        }), 200
    # If login fails, return an error message
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
    

@auth_bp.route('/users', methods=['GET'])
# @jwt_required()
def get_users():
    # Use session.execute with the select() construct
    stmt = select(User)
    users = db.session.execute(stmt).scalars().all()
    
    # Serialise the list of users
    result = users_schema.dump(users)
    return jsonify(result), 200