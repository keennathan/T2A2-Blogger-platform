from datetime import datetime, timezone

from init import db, ma

from marshmallow import fields
from marshmallow.validate import Regexp, Length

# Create media table
class Media(db.Model):
    # The name of the table
    __tablename__ = "media"

    # Attributes of the table
    media_id = db.Column(db.Integer, primary_key=True)
    media_url = db.Column(db.String(255), nullable=False)
    media_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), nullable=False)

    # Relationships of the table
    blog = db.relationship('Blogs', back_populates='media')


class MediaSchema(ma.Schema):
    media_url = fields.String(required=True, validate=Length(max=255))
    media_type = fields.String(required=True, validate=Regexp(r'^(image|video|audio)$', error="Invalid media type"))
    blog_id = fields.Integer(required=True)

     # Nested blog data
    blogs = fields.Nested("BlogSchema", only=["blog_id", "title"])

    class Meta:
        # Fields to include in the output
        fields = ("media_id", "media_url", "media_type", "created_at", "blog_id")
        load_only = ["blog_id"]

# To handle a single media object
media_schema = MediaSchema()
# To handle a list of media objects
medias_schema = MediaSchema(many=True)