from datetime import datetime, timezone

from init import db, ma, bcrypt

from marshmallow import fields
from marshmallow.validate import Length

# Comment table model
class Comments(db.Model):
    # Name of the table
    __tablename__ = "comments"

    # Attributes of the table
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), nullable=False)

    # Relationships of the table
    user = db.relationship("User", back_populates="comments")
    blogs = db.relationship('Blogs', back_populates='comments')

class CommentSchema(ma.Schema):
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