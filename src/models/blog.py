from datetime import datetime, timezone

from init import db, ma, bcrypt
from marshmallow import fields, validate

class Blogs(db.Model):
    """
    Represents a blog post in the database.

    Attributes:
        blog_id (int): The primary key for the blog post.
        title (str): The title of the blog post.
        content (str): The content of the blog post.
        status (str): The status of the blog post (e.g., "draft", "published").
        created_at (datetime): The timestamp when the blog post was created.
        updated_at (datetime): The timestamp when the blog post was last updated.
        user_id (int): The foreign key linking to the User who owns the blog post.

    Relationships:
        user (User): The user who authored the blog post.
        likes (Likes): The likes associated with the blog post.
        comments (Comments): The comments associated with the blog post.
        categories (Category): The categories associated with the blog post (many-to-many).
        media (Media): The media files associated with the blog post.
    """
    # Name of the table 
    __tablename__ = "blogs"

    # Attributes of the table
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="draft")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    # Relationships of the table
    user = db.relationship("User", back_populates="blogs")
    likes = db.relationship("Likes", back_populates="blogs")
    comments = db.relationship("Comments", back_populates="blogs")
    categories = db.relationship('Category', secondary='blog_category', back_populates="blogs")
    media = db.relationship('Media', back_populates='blog', cascade="all, delete-orphan")

class BlogSchema(ma.Schema):
    """
    Schema for validating and serialising Blog objects.

    Validations:
        - title: Must be at least 5 characters long.
        - content: Must be at least 20 characters long.
        - status: Must be either "draft" or "published".
    
    Fields:
        - blog_id: The unique ID of the blog post.
        - title: The title of the blog post.
        - content: The content of the blog post.
        - status: The status of the blog post.
        - created_at: The date and time when the blog was created (read-only).
        - updated_at: The date and time when the blog was last updated (read-only).
        - user: A nested representation of the user who created the blog.
    """
    # Title validation
    title = fields.String(required=True, validate=validate.Length(min=5, error="Title must be at least 5 characters long."))
    # Validate that content is not empty
    content = fields.String(required=True, validate=validate.Length(min=20, error="Content must be at least 20 characters long."))
    # Status validation to allow only draft or published
    status = fields.String(required=True, validate=validate.OneOf(["draft", "published"], error="Status must be 'draft' or 'published'."))
    # Time formatting
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    updated_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    # Foriegn key for user_id
    user_id = fields.Int(dump_only=True)

    # Nested user data
    user = fields.Nested("UserSchema", only=["user_id", "username"])

    class Meta:
        # What will be included in the output
        fields = ("blog_id", "title", "content", "status", "created_at", "updated_at", "user")
        load_only = ["user_id"]

# To handle a single blog object
blog_schema = BlogSchema()
# To handle a list of blog objects
blogs_schema = BlogSchema(many=True)
