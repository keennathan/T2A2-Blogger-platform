from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from utils import admin_required
from models.category import Category, categories_schema, category_schema
from models.blog import Blogs
from models.user import User

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


category_bp = Blueprint('category_bp', __name__, url_prefix='/categories')

# Get the categories
@category_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    try:
        stmt = select(Category)
        result = db.session.execute(stmt).scalars().all()
        return categories_schema.dump(result), 200
    except SQLAlchemyError as e:
        return jsonify({"message": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

# Create a category    
@category_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    try:
        data = request.get_json()
        errors = category_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        # Check if the category already exists
        existing_category = db.session.execute(
            select(Category).where(Category.category_name == data['category_name'])
        ).scalar_one_or_none()

        if existing_category:
            return jsonify({"message": f"Category with name '{data['category_name']}' already exists."}), 409

        new_category = Category(
            category_name=data['category_name']
        )

        db.session.add(new_category)
        db.session.commit()

        return jsonify(category_schema.dump(new_category)), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500
    
# Update a category by id
@category_bp.route('/<int:category_id>', methods= ['PUT','PATCH'])
@jwt_required()
@admin_required
def update_category(category_id):
    try:
        stmt = select(Category).where(Category.category_id == category_id)
        category = db.session.execute(stmt).scalar_one_or_none()

        if not category:
            return jsonify({"message": "Category not found"})
        
        data = request.get_json()

       # Check if 'category_name' is being updated
        if 'category_name' in data:
            # Check if same name exists
            existing_category = db.session.execute(
                select(Category).where(Category.category_name == data['category_name'], Category.category_id != category_id)
            ).scalar_one_or_none()

            # If a category with the same name exists, return an error
            if existing_category:
                return jsonify({"message": "Category name already exists. Please choose a different name."}), 409

            # Update the category name
            category.category_name = data['category_name']

        db.session.commit()

        return category_schema.dump(category), 200  

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    
@category_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_category(id):
    try:

        stmt = select(Category).where(Category.category_id == id)
        category = db.session.execute(stmt).scalar_one_or_none()
        
        if not category:
            return jsonify({"message": "Category not found"}), 404
        
        db.session.delete(category)
        db.session.commit()

        return jsonify({"message": "Category deleted"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    
# Add a blog to a category
@category_bp.route('/<int:category_id>/blogs/<int:blog_id>', methods=['POST'])
@jwt_required()
def add_blog_to_category(category_id, blog_id):
    try:
        stmt_category = select(Category).where(Category.category_id == category_id)
        category = db.session.execute(stmt_category).scalar_one_or_none()
        
        if not category:
            return jsonify({"message": "Category not found"}), 404
        
        stmt_blog = select(Blogs).where(Blogs.blog_id == blog_id)
        blog = db.session.execute(stmt_blog).scalar_one_or_none()
        
        if not blog:
            return jsonify({"message": "Blog not found"}), 404
        
        # Get the current user ID and roles from the JWT
        current_user_id = get_jwt_identity()
        stmt_user = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt_user).scalar_one_or_none()

        # If the user does not exist, return an error
        if not current_user:
            return jsonify({"message": "User not found"}), 404

        # Check if the current user is the blog's author or an Admin/Super Admin
        if blog.user_id != current_user_id and not current_user.has_role("Admin") and not current_user.has_role("Super Admin"):
            return jsonify({"message": "You are not authorized to add this blog to a category"}), 403
        
        # Add the blog to the category's blogs
        if blog not in category.blogs:
            category.blogs.append(blog)
        
        db.session.commit()

        return category_schema.dump(category), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500
    
# Remove a blog from a category
@category_bp.route('/<int:category_id>/blogs/<int:blog_id>', methods=['DELETE'])
@jwt_required()
def remove_blog_from_category(category_id, blog_id):
    try:
        stmt_category = select(Category).where(Category.category_id == category_id)
        category = db.session.execute(stmt_category).scalar_one_or_none()
        
        if not category:
            return jsonify({"message": "Category not found"}), 404
        
        stmt_blog = select(Blogs).where(Blogs.blog_id == blog_id)
        blog = db.session.execute(stmt_blog).scalar_one_or_none()
        
        if not blog:
            return jsonify({"message": "Blog not found"}), 404
        
        # Get the current user ID and roles from the JWT
        current_user_id = get_jwt_identity()
        stmt_user = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt_user).scalar_one_or_none()

        # If the user does not exist, return an error
        if not current_user:
            return jsonify({"message": "User not found"}), 404

        # Check if the current user is the blog's author or an Admin/Super Admin
        if blog.user_id != current_user_id and not current_user.has_role("Admin") and not current_user.has_role("Super Admin"):
            return jsonify({"message": "You are not authorized to add this blog to a category"}), 403
        
        # Remove the blog from the category's blogs
        if blog in category.blogs:
            category.blogs.remove(blog)
        
        db.session.commit()

        return category_schema.dump(category), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500