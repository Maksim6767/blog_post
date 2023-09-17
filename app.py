from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

from auth.routes import auth_bp
from blog.routes import blog_bp

app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)

if __name__ == "__main__":
    app.run(debug=True)
