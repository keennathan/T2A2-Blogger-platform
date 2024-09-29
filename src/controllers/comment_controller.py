from flask import Blueprint, request, jsonify

from init import db
from models.comments import Comments, comments_schema, comment_schema

from sqlalchemy import select
from sqlalchemy.exc import  SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint for comment-related routes
comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

# Create a comment 
@comments_bp.route('/blogs/<int:blog_id>', methods=['POST'])
@jwt_required()
def create_comment(blog_id):
    """
    Creates a new comment on a blog.

    Requires JWT authentication. The current user's ID is extracted from the token.
    
    Args:
        blog_id (int): The ID of the blog the comment is associated with.

    Returns:
        - 201: Comment created successfully.
        - 400: If validation fails or input data is missing.
        - 500: If a database or unexpected error occurs.
    """
    try:
        # Get the current user
        user_id = get_jwt_identity()
        # Load and validate data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Validate the data against the schema
        errors = comment_schema.validate(data, partial=True)
        if errors:
            return jsonify(errors), 400
        
        # Create the new comment instance
        new_comment = Comments(
            content = data.get("content"),
            user_id = user_id,
            blog_id = blog_id
        )

        # Add the comment to the database session and commit
        db.session.add(new_comment)
        db.session.commit()

        # Return the created comment
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
    """
    Retrieves all comments associated with a specific blog.

    Requires JWT authentication.

    Args:
        blog_id (int): The ID of the blog whose comments are to be retrieved.

    Returns:
        - 200: List of comments.
        - 500: If a database or unexpected error occurs.
    """
    try:
        # Query to get all comments for the specified blog
        stmt = select(Comments).where(Comments.blog_id == blog_id)
        comments = db.session.execute(stmt).scalars().all()

        # Return the list of comments
        return comments_schema.dump(comments, many=True), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete a comment 
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """
    Deletes a specific comment.

    Requires JWT authentication. Only the comment's owner can delete it.

    Args:
        comment_id (int): The ID of the comment to delete.

    Returns:
        - 200: Comment deleted successfully.
        - 403: Unauthorized if the user does not own the comment.
        - 404: If the comment is not found.
        - 500: If a database or unexpected error occurs.
    """
    try:
        # Get the current user's ID from the JWT
        user_id = get_jwt_identity()
        # Query to find the comment by its ID
        stmt = select(Comments).where(Comments.comment_id == comment_id)
        comment = db.session.execute(stmt).scalar_one_or_none()

        # Check if the comment exists
        if comment is None:
            return jsonify({"error": "Comment not found"}), 404

        # Check if the user is authorised to delete the comment (must be the owner)
        if comment.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        # Delete the comment from the database and commit
        db.session.delete(comment)
        db.session.commit()

        return jsonify({"message": "Comment deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
