import os

from flask import Flask

from init import db, ma, bcrypt, jwt
from controllers.cli_controllers import db_commands
from controllers.auth_controller import auth_bp
from controllers.blog_controller import blog_bp
from controllers.likes_controller import likes_bp
from controllers.roles_controller import roles_bp
from controllers.comment_controller import comments_bp
from controllers.category_controller import category_bp
from controllers.media_controller import media_bp


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")


    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(likes_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(media_bp)

    return app

