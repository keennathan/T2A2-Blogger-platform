from flask import Blueprint

from init import db, bcrypt
from models.user import User

db_commands = Blueprint("db", __name__)

# To create tables
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print ("Tables created")

# To seed the tables
@db_commands.cli.command("seed")
def seed_tables():
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

    # Commit the changes
    db.session.commit()
    print ("Tables have been seeded")

# To drop the tables
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print ("Tables dropped")