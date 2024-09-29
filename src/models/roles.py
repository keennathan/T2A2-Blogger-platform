from init import db, ma

from marshmallow import fields

class Role(db.Model):
    """
    Represents a role in the system, such as 'Admin', 'Author', etc.

    Attributes:
        role_id (int): The primary key for the role.
        role_name (str): The name of the role (must be unique and not nullable).
    
    Relationships:
        user (User): The users associated with the role (many-to-many relationship through UserRole).
    """
    # The name of the table
    __tablename__ = "roles"
    # Attributes of the table
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), unique=True, nullable=False)

    # Relationship to user through userRole
    user = db.relationship('User', secondary='user_role', back_populates='roles')

class UserRole(db.Model):
    """
    Represents the association between users and roles in a many-to-many relationship.
    
    Attributes:
        user_id (int): Foreign key linking to the User.
        role_id (int): Foreign key linking to the Role.
    """
    # The name of the table
    __tablename__ = "user_role"

    # Attributes of the table
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), primary_key=True)


class RoleSchema(ma.Schema):
    """
    Schema for validating and serialising Role objects.

    Fields:
        role_id (int): The unique ID of the role.
        role_name (str): The name of the role.
    """
    role_id = fields.Int()
    role_name = fields.Str()

# initilise the schemas
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
    