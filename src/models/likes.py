from datetime import datetime, timezone

from init import db, ma

from marshmallow import fields

# Likes table model
class Likes(db.Model):
    __tablename__ = "likes"
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), primary_key=True)

    # Relationships of the table
    user = db.relationship('User', back_populates='likes')
    blogs = db.relationship('Blogs', back_populates='likes')

# Marshmellow schema for serialisation and validation
class LikesSchema(ma.Schema):
    user_id = fields.Integer(required=True)
    blog_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)

likes_schema = LikesSchema()