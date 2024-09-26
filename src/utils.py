from functools import wraps

from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from sqlalchemy import select

from init import db
from models.user import User

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Get the current user from token
        current_user_id = get_jwt_identity()
        # Get the current user from db
        stmt = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt).scalar_one_or_none()

        if not current_user:
            return jsonify({"error": "User not found"}), 404
        
        # Make sure user is Admin or Super Admin
        if not current_user.has_role("Admin") and not current_user.has_role("Super Admin"):
            return jsonify({"error": "Admin access required"}), 403
        
        return f(*args, **kwargs)
    
    return wrapper