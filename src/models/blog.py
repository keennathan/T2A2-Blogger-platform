from datetime import datetime, timezone

from init import db, ma, bcrypt
from marshmallow import fields, Schema, validate

class Blogs(db.Model):
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



class BlogSchema(ma.Schema):
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
