from flask import Blueprint, request, jsonify

from init import db
from models.comments import Comments, CommentSchema, comments_schema, comment_schema
from models.user import UserSchema

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

# Create a comment 
@comments_bp.route('/blogs/<int:blog_id>', methods=['POST'])
@jwt_required()
def create_comment(blog_id):
    try:
        # Get the current user
        user_id = get_jwt_identity()
        # Load and validate data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        errors = comment_schema.validate(data, partial=True)
        if errors:
            return jsonify(errors), 400
        
        new_comment = Comments(
            content = data.get("content"),
            user_id = user_id,
            blog_id = blog_id
        )

        db.session.add(new_comment)
        db.session.commit()

        return comment_schema.jsonify(new_comment), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500 
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Get comments from a blog
@comments_bp.route('/blogs/<int:blog_id>', methods=['GET'])
@jwt_required()
def get_blog_comments(blog_id):
    try:
        stmt = select(Comments).where(Comments.blog_id == blog_id)
        comments = db.session.execute(stmt).scalars().all()

        return comments_schema.dump(comments, many=True), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete a comment 
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    try:
        user_id = get_jwt_identity()

        stmt = select(Comments).where(Comments.comment_id == comment_id)
        comment = db.session.execute(stmt).scalar_one_or_none()

        if comment is None:
            return jsonify({"error": "Comment not found"}), 404

        if comment.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        db.session.delete(comment)
        db.session.commit()

        return jsonify({"message": "Comment deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
