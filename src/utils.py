from functools import wraps

from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from sqlalchemy import select

from init import db
from models.user import User

def admin_required(f):
    """
    Decorator to ensure that a user has 'Admin' or 'Super Admin' role.
    
    This decorator checks if the current user, based on the JWT token, has the required 
    admin privileges. It first retrieves the user's identity from the token, then fetches 
    the user from the database. If the user does not have 'Admin' or 'Super Admin' roles, 
    access to the route is denied.
    
    Returns:
        - If the user is authenticated and has the correct role(s), the wrapped route 
          function is executed.
        - If the user is not authenticated or lacks the required role, an appropriate 
          error response is returned.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Get the current user from token
        current_user_id = get_jwt_identity()
        # Get the current user from db
        stmt = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt).scalar_one_or_none()

        # If the user is not found in the database, return a 404 error
        if not current_user:
            return jsonify({"error": "User not found"}), 404
        
        # Make sure user is Admin or Super Admin
        if not current_user.has_role("Admin") and not current_user.has_role("Super Admin"):
            return jsonify({"error": "Admin access required"}), 403
        
        # If the user is authorised, proceed with executing the wrapped route function
        return f(*args, **kwargs)
    
    return wrapper