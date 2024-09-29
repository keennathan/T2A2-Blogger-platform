import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from init import db
from utils import admin_required
from models.category import Category, categories_schema, category_schema, CategorySchema
from models.blog import Blogs
from models.media import Media, media_schema, medias_schema
from models.user import User

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

media_bp = Blueprint("media", __name__, url_prefix="/media")

# Path to the upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Allowed extensions for file uploads
ALLOWED_EXTENSIONS = {
    'mp4', 'avi', 'mov', 'mkv', 'webm',  # Video
    'png', 'jpg', 'jpeg', 'gif', 'webp',  # Images
    'mp3', 'wav', 'ogg'  # Audio
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload media file
@media_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_media():
    try:
        # Get the current user
        current_user_id = get_jwt_identity()

        # check if file was sent
        if 'file' not in request.files or not request.form.get('blog_id'):
            return jsonify({"error": "No file or blog ID provided"}), 400
        
        file = request.files['file']
        blog_id = request.form.get('blog_id')

        # make sure file is selected and is an allowed type
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({"error": "No selected file or file type not allowed"}), 400
        
        # check the blog owner
        stmt = select(Blogs).where(Blogs.blog_id == blog_id)
        blog = db.session.execute(stmt).scalar_one_or_none()

        if not blog:
            return jsonify({"error": "Blog not found"}), 404
        
        # Ensure the current user is the owner of the blog
        if blog.user_id != current_user_id:
            return jsonify({"error": "You do not have permission to upload media to this blog"}), 403

        # Secure the filename and save it
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Save the file to the uploads folder
        file.save(file_path)

        # Create new media record
        media = Media(
                media_url=file_path,
                media_type=file.content_type.split('/')[0], 
                blog_id=blog_id
            )
        db.session.add(media)
        db.session.commit()

        return media_schema.dump(media), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get media by id
@media_bp.route('/<int:media_id>', methods=['GET'])
@jwt_required()
def get_media(media_id):
    stmt = select(Media).where(Media.media_id == media_id)
    media = db.session.execute(stmt).scalar_one_or_none()

    if not media:
        return jsonify({"error": "Media not found"}), 404
    
    return media_schema.dump(media), 200

# get the media by blog
@media_bp.route('/blog/<int:blog_id>', methods=['GET'])
@jwt_required()
def get_media_by_blog(blog_id):
    stmt = select(Media).where(Media.blog_id == blog_id)
    media = db.session.execute(stmt).scalars().all()

    if not media:
        return jsonify({"error": "No media found for this blog post"}), 404
    
    return medias_schema.dump(media), 200

# delete the media, only the author or admin or super admin
@media_bp.route('/<int:media_id>', methods=['DELETE'])
@jwt_required()
def delete_media(media_id):
    try:
        # Get the current user
        current_user_id = get_jwt_identity()
        
        # Find the media by id
        stmt = select(Media).where(Media.media_id == media_id)
        media = db.session.execute(stmt).scalar_one_or_none()

        if not media:
            return jsonify({"error": "Media not found"}), 404
        
        # Get the current user from db
        stmt = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt).scalar_one_or_none()

        if not current_user:
            return jsonify({"error": "User not found"}), 404
        
         # Check if the current user is the author of the media
        is_author = media.blog.user_id == current_user.user_id
        
        # Check if the current user has admin or super_admin roles using has_role function
        is_admin = current_user.has_role('Admin') or current_user.has_role('Super Admin')
        
        # Only allow if the user is the author or has admin/super_admin role
        if not (is_author or is_admin):
            return jsonify({"error": "You do not have permission to delete this media"}), 403
            
        # Delete the media record from the database
        db.session.delete(media)
        db.session.commit()

        # delete the file from the filesystem
        if os.path.exists(media.media_url):
            os.remove(media.media_url)

        return jsonify({"message": "Media deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500