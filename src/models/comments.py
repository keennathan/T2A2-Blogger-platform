from datetime import datetime, timezone

from models.roles import RoleSchema
from init import db, ma, bcrypt

from marshmallow import fields
from marshmallow.validate import Regexp, Length

# Comment table model
class Comments(db.Model):
    # Name of the table
    __tablename__ = "comments"

    # Attributes of the table
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), primary_key=True)

    # Relationships of the table
    user = db.relationship("User", back_populates="comments")
    blogs = db.relationship('Blogs', back_populates='comments')