from datetime import datetime, timezone

from init import db, ma

from marshmallow import fields

# Likes table model
class Likes(db.Model):
    """
    Represents a 'like' on a blog post by a user.

    Attributes:
        created_at (datetime): The timestamp when the like was created.
        user_id (int): The ID of the user who liked the blog post.
        blog_id (int): The ID of the blog post that was liked.
    
    Relationships:
        user (User): The user who liked the blog post.
        blogs (Blogs): The blog post that was liked.
    """
    __tablename__ = "likes"
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), primary_key=True)

    # Relationships of the table
    user = db.relationship('User', back_populates='likes')
    blogs = db.relationship('Blogs', back_populates='likes')

# Marshmellow schema for serialisation and validation
class LikesSchema(ma.Schema):
    """
    Schema for validating and serialising Likes objects.

    Fields:
        user_id (int): The ID of the user who liked the blog (required).
        blog_id (int): The ID of the blog post that was liked (required).
        created_at (datetime): The timestamp when the like was created (read-only).
    """
    user_id = fields.Integer(required=True)
    blog_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    
# Instance of LikesSchema for handling a single Like object
likes_schema = LikesSchema()