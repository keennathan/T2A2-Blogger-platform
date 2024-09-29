from init import db, ma
from models.blog import BlogSchema, Blogs

from marshmallow import fields, Schema

# Category table model
class Category(db.Model):
    # Table name
    __tablename__ = "categories"

    # Attributes of the table
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), unique=True, nullable=False)

    # relationships of the table
    blogs = db.relationship('Blogs', secondary='blog_category', back_populates="categories")

class BlogCategory(db.Model):
    # Table name
    __tablename__ = "blog_category"

    # Attributes of the table
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), primary_key=True)

class CategorySchema(Schema):
    category_id = fields.Int(dump_only=True)
    category_name = fields.Str(required=True)
    blogs = fields.List(fields.Nested(BlogSchema, only=('blog_id', 'title', 'status')))

    class Meta:
        fields = ("category_id", "category_name", "blogs")


# To handle a single category object
category_schema = CategorySchema()
# To handle a list of category objects
categories_schema = CategorySchema(many=True)