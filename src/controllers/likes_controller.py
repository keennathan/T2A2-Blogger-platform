from flask import Blueprint, request, jsonify

from init import db
from models.likes import likes_schema, Likes
from models.user import User, user_schema
from models.blog import Blogs

from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, func

# Blueprint for likes
likes_bp = Blueprint('likes', __name__, url_prefix='/likes')

# Add a like
@likes_bp.route('/', methods=['POST'])
@jwt_required()
def add_like():
    try:
        # Get the user from JWT
        current_user_id = get_jwt_identity()
        data = request.get_json()
        blog_id = data.get("blog_id")

        if not blog_id:
            return jsonify({"error": "Blog_id is required"}), 400
        
        # Check if a like already exists
        stmt = select(Likes).where(Likes.user_id == current_user_id, Likes.blog_id == blog_id)
        existing_like = db.session.execute(stmt).scalars().first()
        if existing_like:
            return jsonify({"message": "Already liked"}), 400
        
        # Create a new like 
        new_like = Likes(user_id=current_user_id, blog_id=blog_id)
        db.session.add(new_like)
        db.session.commit()

        return jsonify({"message": "Like added"}), 201
    
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Invalid blog_id"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    
# Remove a like
@likes_bp.route('/', methods=['DELETE'])
@jwt_required()
def remove_like():
    try:
         # Get the user from JWT
        current_user_id = get_jwt_identity()
        data = request.get_json()
        blog_id = data.get("blog_id")

        if not blog_id:
            return jsonify({"error": "Blog_id is required"}), 400
        
        # Find and delete the like
        stmt = select(Likes).where(Likes.user_id == current_user_id, Likes.blog_id == blog_id)
        like = db.session.execute(stmt).scalars().first()
        if not like:
            return jsonify({"message": "Like not found"}), 404
        
        db.session.delete(like)
        db.session.commit()

        return jsonify({"message": "Like removed successfully"}), 200
    
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Invalid blog_id"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    
# Get all the users who liked a blog
@likes_bp.route('/users/blog/<int:blog_id>', methods=['GET'])
@jwt_required()
def get_likes_for_blog(blog_id):
    try:
        stmt = select(User).join(Likes).where(Blogs.blog_id == blog_id)
        users = db.session.execute(stmt).scalars().all()

        if not users:
            return jsonify({"message": "No users found who liked this blog"}), 404

        return jsonify(user_schema.dump(users, many=True)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

# Get total likes for a blog
@likes_bp.route('/count/blog/<int:blog_id>', methods=['GET'])
def get_total_likes_for_blog(blog_id):
    try:
        stmt = select(func.count(Likes.created_at)).where(Likes.blog_id == blog_id)
        total = db.session.execute(stmt).scalar()

        if total is None:
            return jsonify({"message": "No likes found for this blog"}), 404

        return jsonify({"total_likes": int(total)}), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

# Get all liked blogs for current user
@likes_bp.route('/blogs/user', methods=['GET'])
@jwt_required()
def get_liked_blogs_for_user():
    try:
        current_user = get_jwt_identity()
        stmt = select(Blogs).join(Likes).where(Likes.user_id == current_user)
        liked_blogs = db.session.execute(stmt).scalars().all()

        if not liked_blogs:
            return jsonify({"message": "No blogs liked by the current user"}), 404

        return jsonify(likes_schema.dump(liked_blogs, many=True)), 200 
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500