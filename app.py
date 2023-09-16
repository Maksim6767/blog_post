from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
import os
import secrets

from auth import *
from controllers import *

JWT_SECRET_KEY = secrets.token_hex(32)
os.environ["JWT_SECRET_KEY"] = JWT_SECRET_KEY

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db = SQLAlchemy(app)

from models import User, BlogPost

jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(debug=True)
