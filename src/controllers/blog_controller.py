from flask import Blueprint, request, jsonify

from init import db
from models.blog import Blogs, blog_schema, blogs_schema
from models.user import User

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

# Blueprint for blogs
blog_bp = Blueprint('blogs', __name__, url_prefix='/blogs')

# To create a new blog(only Authors, Admin, Super Admin)
@blog_bp.route("/", methods=["POST"])
@jwt_required()
def create_blog():
    """
    Creates a new blog post in the system.
    
    Only users with the 'Author', 'Admin', or 'Super Admin' roles can create blogs.
    
    Returns:
        - 201: Blog created successfully.
        - 403: If the user does not have permission to create a blog.
        - 404: If the current user is not found.
        - 400: If validation errors occur with the request data.
        - 500: If an integrity error or other server error occurs.
    """
    try:
        # Get the current user from JWT
        current_user_id = get_jwt_identity()
        stmt = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt).scalar_one_or_none()

        if not current_user:
            return jsonify({"error": "User not found"}), 404
        
        # Check if the user has the right role
        if not (current_user.has_role('Author') or current_user.has_role('Admin') or current_user.has_role('Super Admin')):
            return jsonify({"message": "you do not have permission to create a blog"}), 403
        
        # Parse and validate request data
        blog_data = blog_schema.load(request.get_json())

        # Create a new blog post
        new_blog = Blogs(
            title = blog_data["title"],
            content = blog_data["content"],
            status = blog_data["status"],
            user_id = current_user.user_id
        )

        # Save to DB
        db.session.add(new_blog)
        db.session.commit()

        result = blog_schema.dump(new_blog)
        return jsonify({"message": "Blog created successfully!", "blog": result}), 201
    
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# route to filter by status of blogs
@blog_bp.route('/status/<string:status>', methods=['GET'])
@jwt_required()
def get_blogs_by_status(status):
    """
    Retrieves blogs filtered by their status.
    
    Args:
        status (str): The status of the blogs to retrieve (e.g., 'published', 'draft').
    
    Returns:
        - 200: Blogs retrieved successfully.
        - 404: If no blogs with the given status are found.
        - 500: For any other server errors.
    """
    try:
        # select blogs by status
        stmt = select(Blogs).where(Blogs.status == status)
        result = db.session.execute(stmt).scalars().all()

        # If no blogs are found
        if not result:
            return jsonify({"message": f"No blogs found with status '{status}'"}), 404
        
        return jsonify(blogs_schema.dump(result)), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to list of blogs by a specific user
@blog_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_blogs_by_user(user_id):
    try:
        """
    Retrieves all blogs created by a specific user.
    
    Args:
        user_id (int): The ID of the user whose blogs are to be retrieved.
    
    Returns:
        - 200: Blogs retrieved successfully.
        - 404: If the user or their blogs are not found.
        - 500: For any other server errors.
    """
        # Select the user by user_id
        stmt = select(User).where(User.user_id == user_id)
        user = db.session.execute(stmt).scalar_one_or_none()

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Select all the blogs of the user
        stmt = select(Blogs).where(Blogs.user_id == user_id)
        blogs = db.session.execute(stmt).scalars().all()

        if not blogs:
            return jsonify({"message": "No blogs where found for this user"}), 404
        
        return jsonify(blogs_schema.dump(blogs)), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get a single blog
@blog_bp.route('/<int:blog_id>', methods=['GET'])
@jwt_required()
def get_blog(blog_id):
    try:
        """
    Retrieves a single blog by its ID.
    
    Args:
        blog_id (int): The ID of the blog to retrieve.
    
    Returns:
        - 200: Blog retrieved successfully.
        - 404: If the blog is not found.
        - 500: For any other server errors.
    """
        # create the select statement 
        stmt = select(Blogs).where(Blogs.blog_id == blog_id)
        result = db.session.execute(stmt).scalar()

        # if no blog is found
        if result is None:
            return jsonify({"message": "Blog not found"}), 404
        
        return jsonify(blog_schema.dump(result)), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to update a blog (Only Author of the blog, Admin, Super Admin)   
@blog_bp.route('/<int:blog_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_blog(blog_id):
    """
    Updates a blog post.
    
    Only the author of the blog or users with 'Admin' or 'Super Admin' roles can update the blog.
    
    Args:
        blog_id (int): The ID of the blog to update.
    
    Returns:
        - 200: Blog updated successfully.
        - 403: If the user does not have permission to update the blog.
        - 404: If the blog or current user is not found.
        - 400: If validation errors occur with the request data.
        - 500: For any other server errors.
    """
    try:
        # Get the user from JWT
        current_user_id = get_jwt_identity()
        stmt = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt).scalar_one_or_none()

        if not current_user:
            return jsonify({"error": "User not found"}), 404
        
        # Get the blog to be updated
        stmt = select(Blogs).where(Blogs.blog_id == blog_id)
        blog = db.session.execute(stmt).scalar_one_or_none()

        if not blog:
            return jsonify({"error": "Blog not found"}), 404
        
        # Check the user is the author or an Admin or Super Admin
        if blog.user_id != current_user.user_id and not (current_user.has_role("Admin") or current_user.has_role("Super Admin")):
            return jsonify({"error": "You can only update your own blog or must be an Admin or Super Admin"}), 403
        
        # Parse and validate the request data
        blog_data = blog_schema.load(request.get_json(), partial=True)

        # update the blog
        blog.title = blog_data.get("title", blog.title)
        blog.content = blog_data.get("content", blog.content)
        blog.status = blog_data.get("status", blog.status)

        # Save the update
        db.session.commit()
        result = blog_schema.dump(blog)

        return jsonify({"message": "Blog updated successfully", "blog": result}), 200
    
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Route to delete a blog (Only the Author or Admin or Super Admin)
@blog_bp.route('/<int:blog_id>', methods=['DELETE'])
@jwt_required()
def delete_blog(blog_id):
    """
    Deletes a blog post.
    
    Only the author of the blog or users with 'Admin' or 'Super Admin' roles can delete the blog.
    
    Args:
        blog_id (int): The ID of the blog to delete.
    
    Returns:
        - 200: Blog deleted successfully.
        - 403: If the user does not have permission to delete the blog.
        - 404: If the blog or current user is not found.
        - 500: For any other server errors.
    """
    try:
        # Get the user from JWT
        current_user_id = get_jwt_identity()
        stmt = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt).scalar_one_or_none()

        if not current_user:
            return jsonify({"error": "User not found"}), 404
        
        # Get the blog to be deleted
        stmt = select(Blogs).where(Blogs.blog_id == blog_id)
        blog = db.session.execute(stmt).scalar_one_or_none()

        if not blog:
            return jsonify({"error": "Blog not found"}), 404
        
        # get the Author of the blog
        stmt = select(User).where(User.user_id == blog.user_id)
        blog_author = db.session.execute(stmt).scalar_one_or_none()

        # Check the user is the author 
        if blog.user_id == current_user.user_id:
            # Author can only delete thier own blog, not if is from an admin or super admin
            if blog_author.has_role("Admin") or blog_author.has_role("Super Admin"):
                return jsonify({"error": "You cannot delete a blog created by an Admin or Super Admin"}), 403
            else:
                db.session.delete(blog)
                db.session.commit()
                return jsonify({"message": "Blog deleted successfully"}), 200
            
        # Admins and super admins can delete any blog
        elif current_user.has_role("Admin") or current_user.has_role("Super Admin"):
            db.session.delete(blog)
            db.session.commit()
            return jsonify({"message": "Blog deleted successfully"}), 200
        else:
            return jsonify({"error": "You can only delete your own blog or must be an Admin or Super Admin"}), 403
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

