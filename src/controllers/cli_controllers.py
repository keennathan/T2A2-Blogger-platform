from flask import Blueprint
from sqlalchemy import select

from init import db, bcrypt
from models.user import User
from models.roles import Role
from models.blog import Blogs
from models.category import Category

db_commands = Blueprint("db", __name__)

# To create tables
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print ("Tables created")

# To seed the tables
@db_commands.cli.command("seed")
def seed_tables():
    try:
        # Create the user instance
        user1 = User(
            username = "john",
            email = "john@email.com"
        )
        user1.set_password("abc123")

        # Create the user instance
        user2 = User(
            username = "pam",
            email = "pam@email.com"
        )
        user2.set_password("123abc")

        # Create a list of users
        users = [user1, user2]

        # Add the users to the session
        db.session.add_all(users)

        # Creating the roles to be seeded
        role_names = ['Super Admin', 'Admin', 'Author', 'Reader']
        roles = []

        for role_name in role_names:
            role = Role(role_name=role_name)
            roles.append(role)

        db.session.add_all(roles)

        user1.roles.append(roles[0])
        user2.roles.append(roles[1])

        # Create the test blogs
        blog1 = Blogs(
                title="First Blog Post",
                content="This is the content of the first blog post.",
                status="published",
                user=user1)
        blog2 = Blogs(
            title="Second Blog Post",
            content="This is the content of the second blog post.",
            status="draft",
            user=user2)
        blog3 = Blogs(
            title="Third Blog Post",
            content="This is the content of the third blog post.",
            status="published",
            user=user2)
        # Add the blogs to the session
        db.session.add(blog1)
        db.session.add(blog2)
        db.session.add(blog3)

        # Add categories to be seeded
        categories = [
            "Technology", "Lifestyle", "Travel", "Food", "Education",
            "Health & Fitness", "Entertainment", "Business", "Finance",
            "Fashion", "Sports", "News", "Science", "DIY & Crafts", "Personal Development"
        ]
        for category_name in categories:
                stmt = select(Category).where(Category.category_name == category_name)
                existing_category = db.session.execute(stmt).scalar_one_or_none()
                
                if not existing_category:
                    category = Category(category_name=category_name)
                    db.session.add(category)

        # Link blogs to categories
        blog1.categories.append(db.session.execute(select(Category).where(Category.category_name == "Technology")).scalar_one())
        blog2.categories.append(db.session.execute(select(Category).where(Category.category_name == "Lifestyle")).scalar_one())
        blog3.categories.append(db.session.execute(select(Category).where(Category.category_name == "Travel")).scalar_one())

        # Commit the changes
        db.session.commit()
        print ("Tables have been seeded")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding the tables: {e}")

# To drop the tables
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print ("Tables dropped")