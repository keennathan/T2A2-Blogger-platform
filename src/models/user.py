from datetime import datetime, timezone

from models.roles import RoleSchema
from init import db, ma, bcrypt

from marshmallow import fields
from marshmallow.validate import Regexp, Length


# User table model
class User(db.Model):
    """
    Represents a user in the system, including their credentials and related data.

    Attributes:
        user_id (int): The primary key for the user.
        username (str): The unique username of the user.
        email (str): The unique email address of the user.
        password_hash (str): The hashed password of the user.
        created_at (datetime): The timestamp when the user was created.
    
    Relationships:
        roles (Role): The roles associated with the user (many-to-many).
        blogs (Blogs): The blogs authored by the user (one-to-many).
        likes (Likes): The likes made by the user (one-to-many).
        comments (Comments): The comments made by the user (one-to-many).
    
    Methods:
        set_password(password): Hashes and sets the user's password.
        check_password(password): Checks if the provided password matches the stored hash.
        has_role(role_name): Checks if the user has a specific role.
    """
    # The name of the table
    __tablename__ = "users"  

    # Attributes of the table
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships of the table
    roles = db.relationship('Role', secondary='user_role', back_populates='user')
    blogs = db.relationship('Blogs', back_populates='user', lazy='dynamic')
    likes = db.relationship('Likes', back_populates='user')
    comments = db.relationship('Comments', back_populates='user')

    # To set a password
    def set_password(self, password):
        """
        Hashes and sets the user's password.

        Args:
            password (str): The plaintext password to be hashed and stored.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    #To check the password
    def check_password(self, password):
        """
        Verifies the password against the stored password hash.

        Args:
            password (str): The plaintext password to be checked.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password_hash, password)
    
    # To check if user has a specific role
    def has_role(self, role_name):
        """
        Checks if the user has a specific role.

        Args:
            role_name (str): The name of the role to check.

        Returns:
            bool: True if the user has the role, False otherwise.
        """
        return any(role.role_name == role_name for role in self.roles)
    

class UserSchema(ma.Schema):
    """
    Schema for validating and serializing User objects.

    Validations:
        - email: Must be a valid email address.
        - new_password: Must be at least 6 characters long.
    
    Fields:
        email (str): The user's email address (required, validated).
        new_password (str): The user's new password (used for input only, validated).
        old_password (str): The user's current password (used for input only).
        created_at (datetime): The timestamp when the user was created (read-only).
        roles (list): The roles assigned to the user (read-only).
    """
    # Email validation with regular expression
    email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format."))

    # Password validation
    new_password = fields.String(
        required=True,
        validate=Length(min=6, error="Password should be at least 6 characters long"),
        # This will ensure that the password is only used for input and not output
        load_only=True  
    )
    # Old password for verification during password change
    old_password = fields.String(load_only=True)

    # Timestamp formatting for output
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    # Nested roles for user, using the RoleSchema
    roles = fields.Nested(RoleSchema, many=True)

    class Meta:
        # Fields to include in the serialised output
        fields = ("user_id", "username", "email", "created_at", "roles", "new_password", "old_password")
        load_only = ["new_password", "old_password"]


# to handle a single user object
user_schema = UserSchema()

# to handle a list of user objects
users_schema = UserSchema(many=True)