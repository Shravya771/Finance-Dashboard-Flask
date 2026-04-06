from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "")
    # FIX: normalize role to lowercase so frontend values like "Viewer" are accepted
    role = data.get("role", "").strip().lower()

    if not username or not password or not role:
        return jsonify({"msg": "All fields are required"}), 400

    if role not in ["viewer", "analyst", "admin"]:
        return jsonify({"msg": "Invalid role. Must be viewer, analyst, or admin"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(username=username, password=hashed_password, role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": token,
        "role": user.role
    }), 200