from flask import Blueprint, request, jsonify

from init import db
from models.blog import Blogs, blog_schema, blogs_schema
from models.user import User

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from flask import abort

# Blueprint for blogs
blog_bp = Blueprint('blogs', __name__, url_prefix='/blogs')

# To create a new blog(only Authors, Admin, Super Admin)
@blog_bp.route("/", methods=["POST"])
@jwt_required()
def create_blog():
    try:
        # Get the current user
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
    
# route to get all the published blogs
@blog_bp.route('/', methods=['GET'])
@jwt_required()
def get_published_blogs():
    try:
        # select to get only published blogs
        stmt = select(Blogs).where(Blogs.status == 'published')
        result = db.session.execute(stmt).scalars().all()

        # If no published blogs are found
        if not result:
            return jsonify({"message": "No published blogs found"}), 404
        
        return jsonify(blogs_schema.dump(result)), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get a single blog
@blog_bp.route('/<int:blog_id>', methods=['GET'])
@jwt_required()
def get_blog(blog_id):
    try:
        # create the select statement 
        stmt = select(Blogs).where(Blogs.blog_id == blog_id)
        result = db.session.execute(stmt).scalar()

        # if no blog is found
        if result is None:
            return jsonify({"message": "Blog not found"}), 404
        
        return jsonify(blog_schema.dump(result)), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500