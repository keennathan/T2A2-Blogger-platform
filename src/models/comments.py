from datetime import datetime, timezone

from init import db, ma, bcrypt

from marshmallow import fields
from marshmallow.validate import Length

# Comment table model
class Comments(db.Model):
    """
    Represents a comment on a blog post in the database.

    Attributes:
        comment_id (int): The primary key for the comment.
        content (str): The text content of the comment.
        created_at (datetime): The timestamp when the comment was created.
        updated_at (datetime): The timestamp when the comment was last updated.
        user_id (int): The foreign key linking to the User who authored the comment.
        blog_id (int): The foreign key linking to the Blog the comment belongs to.
    
    Relationships:
        user (User): The user who authored the comment.
        blogs (Blogs): The blog post the comment is associated with.
    """
    # Name of the table
    __tablename__ = "comments"

    # Attributes of the table
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    # Foreign keys linking to User and Blog
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), nullable=False)

    # Relationships of the table
    user = db.relationship("User", back_populates="comments")
    blogs = db.relationship('Blogs', back_populates='comments')

class CommentSchema(ma.Schema):
    """
    Schema for validating and serialising Comment objects.

    Validations:
        - content: Must be between 1 and 500 characters long.
    
    Fields:
        - comment_id: The unique ID of the comment (read-only).
        - content: The text content of the comment (required).
        - created_at: The timestamp when the comment was created (read-only).
        - updated_at: The timestamp when the comment was last updated (read-only).
        - user: Nested data of the user who authored the comment (read-only).
        - blog_id: The ID of the blog post the comment is associated with (load-only).
    """
    # validation 
    content = fields.String(required=True, validate=Length(min=1, max=500))
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    updated_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)

    # Nested relationship data
    user = fields.Nested("UserSchema", only=["user_id", "username"], dump_only=True)
    blog_id = fields.Int(load_only=True)

    class Meta:
        # What will be included in the output
        fields = ("comment_id", "content", "created_at", "updated_at", "user", "blog_id")
        load_only = ["blog_id"]

# Single comment schema and list of comments schema
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)