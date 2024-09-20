from init import db

from marshmallow import fields, Schema

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), unique=True, nullable=False)

    # Relationship to user through userRole
    users = db.relationship('User', secondary='user_role', back_populates='roles')

class UserRole(db.Model):
    __tablename__ = "user_role"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)


class RoleSchema(Schema):
    id = fields.Int()
    role_name = fields.Str()