from datetime import datetime, timezone

from init import db, ma, bcrypt
from marshmallow import fields
from marshmallow.validate import Regexp

class User(db.Model):
    # The name of the table
    __tablename__ = "users"  

    # Attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships of the table


    # To set a password
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    #To check the password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    

class UserSchema(ma.Schema):


    email = fields.String(required=True, validate=Regexp("^\S+@\S+\.\S+$", error="Invalid Email Format."))

    class Meta:
        fields = ("id", "username", "email", "password_hash", "create_at")


# to handle a single user object
user_schema = UserSchema(exclude=["password_hash"])

# to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password_hash"])