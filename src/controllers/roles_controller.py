from flask import Blueprint, jsonify,request
from sqlalchemy import select
from flask_jwt_extended import jwt_required

from init import db
from utils import admin_required
from models.roles import Role, role_schema, roles_schema
from models.user import User

# Blueprint for roles
roles_bp = Blueprint('roles', __name__, url_prefix='/roles')

# Read all the roles
@roles_bp.route('/', methods=['GET'])
def get_roles():
    try:
        stmt = select(Role)
        roles = db.session.execute(stmt).scalars().all()
        roles_data = roles_schema.dump(roles)

        return roles_schema.dump(roles_data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Assign a role to a user, only if you are a Admin or super admin
@roles_bp.route('/assign', methods=['POST'])
@jwt_required()
@admin_required
def assign_role():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        role_id = data.get("role_id")

        if not user_id or not role_id:
            return jsonify({"error": "user_id and role_id are required"}), 400
        
        # Get the user and role
        user_stmt = select(User).where(User.user_id == user_id)
        role_stmt = select(Role).where(Role.role_id == role_id)

        user = db.session.execute(user_stmt).scalar_one_or_none()
        role = db.session.execute(role_stmt).scalar_one_or_none()

        if not user:
            return jsonify({"error": "User not found"}), 404
        if not role:
            return jsonify({"error": "Role not found"}), 404
        
        # Check the user has role already
        if user.has_role(role.role_name):
            return jsonify({"error": "User already has this role"}), 400
        
        user.roles.append(role)
        db.session.commit()

        return jsonify({"message": "Role assigned successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# CREATE a new role (admin only)
@roles_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_role():
    try:
        data = request.get_json()
        role_name = data.get("role_name")

        # Ensure role_name is provided
        if not role_name:
            return jsonify({"error": "role_name is required"}), 400

        # Check if the role already exists
        stmt = select(Role).where(Role.role_name == role_name)
        existing_role = db.session.execute(stmt).scalar_one_or_none()

        if existing_role:
            return jsonify({"error": "Role already exists"}), 400

        # Create a new role
        new_role = Role(role_name=role_name)
        db.session.add(new_role)
        db.session.commit()

        role_data = role_schema.dump(new_role)
        return jsonify(role_data), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Update an existing role (admin only)
@roles_bp.route('/<int:role_id>', methods=['PUT','PATCH'])
@jwt_required()
@admin_required
def update_role(role_id):
    try:
        stmt = select(Role).where(Role.role_id == role_id)
        role = db.session.execute(stmt).scalar_one_or_none()

        if not role:
            return jsonify({"error": "Role not found"}), 404

        # Get the new role name
        data = request.get_json()
        new_role_name = data.get("role_name")

        if not new_role_name:
            return jsonify({"error": "role_name is required"}), 400

        # Check if another role with the new name already exists
        stmt = select(Role).where(Role.role_name == new_role_name)
        existing_role = db.session.execute(stmt).scalar_one_or_none()

        if existing_role:
            return jsonify({"error": "Role name already exists"}), 400

        # Update the role name
        role.role_name = new_role_name
        db.session.commit()

        role_data = role_schema.dump(role)
        return jsonify(role_data), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Delete an existing role (admin only)
@roles_bp.route('/<int:role_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_role(role_id):
    try:
        stmt = select(Role).where(Role.role_id == role_id)
        role = db.session.execute(stmt).scalar_one_or_none()

        if not role:
            return jsonify({"error": "Role not found"}), 404

        db.session.delete(role)
        db.session.commit()

        return jsonify({"message": "Role deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500