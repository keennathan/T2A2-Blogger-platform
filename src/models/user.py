from datetime import datetime, timezone

from init import db, ma, bcrypt
from marshmallow import fields
from marshmallow.validate import Regexp, Length

from models.roles import RoleSchema

class User(db.Model):
    # The name of the table
    __tablename__ = "users"  

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships of the table
    roles = db.relationship('Role', secondary='user_role', back_populates='users')

    # To set a password
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    #To check the password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    # To check if user has a specific role
    def has_role(self, role_name):
        return any(role.role_name == role_name for role in self.roles)
    

class UserSchema(ma.Schema):

    email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format."))

    # Password validation
    password = fields.String(
        required=True,
        validate=Length(min=6, error="Password should be at least 6 characters long"),
        # This will ensure that the password is only used for input and not output
        load_only=True  
    )
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    roles = fields.Nested(RoleSchema, many=True)

    class Meta:
        fields = ("id", "username", "email", "created_at", "roles")
        load_only = ["password"]


# to handle a single user object
user_schema = UserSchema()

# to handle a list of user objects
users_schema = UserSchema(many=True)