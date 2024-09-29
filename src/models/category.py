from init import db, ma
from models.blog import BlogSchema

from marshmallow import fields, Schema

# Category table model
class Category(db.Model):
    """
    Represents a category in the database.

    Attributes:
        category_id (int): The primary key for the category.
        category_name (str): The name of the category (must be unique).
    
    Relationships:
        blogs (Blogs): The blogs associated with the category (many-to-many relationship).
    """
    # Table name
    __tablename__ = "categories"

    # Attributes of the table
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), unique=True, nullable=False)

    # relationships of the table
    blogs = db.relationship('Blogs', secondary='blog_category', back_populates="categories")

class BlogCategory(db.Model):
    """
    Represents the association table between blogs and categories.
    
    Attributes:
        category_id (int): Foreign key to the Category.
        blog_id (int): Foreign key to the Blog.
    """
    # Table name
    __tablename__ = "blog_category"

    # Attributes of the table
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.blog_id'), primary_key=True)

class CategorySchema(Schema):
    """
    Schema for validating and serialising Category objects.

    Fields:
        category_id (int): The unique ID of the category (read-only).
        category_name (str): The name of the category (required).
        blogs (list): A list of nested Blog objects related to the category.
    """
    category_id = fields.Int(dump_only=True)
    category_name = fields.Str(required=True)

    # Nested list of blogs associated with the category
    blogs = fields.List(fields.Nested(BlogSchema, only=('blog_id', 'title', 'status')))

    class Meta:
        # Fields to include in the output
        fields = ("category_id", "category_name", "blogs")


# To handle a single category object
category_schema = CategorySchema()
# To handle a list of category objects
categories_schema = CategorySchema(many=True)