from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Transaction
from app import db
from app.utils.decorators import role_required

user_bp = Blueprint("users", __name__)


# ===============================
# GET ALL USERS
# ===============================
@user_bp.route("/", methods=["GET"])
@jwt_required()
@role_required(["admin"])
def get_all_users():
    users = User.query.all()

    result = [{
        "id": u.id,
        "username": u.username,
        "role": u.role
    } for u in users]

    return jsonify(result), 200


# ===============================
# UPDATE USER ROLE
# ===============================
@user_bp.route("/<int:id>/role", methods=["PUT"])
@jwt_required()
@role_required(["admin"])
def update_role(id):
    data = request.get_json()

    if not data or "role" not in data:
        return jsonify({"msg": "Role is required"}), 400

    user = User.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    valid_roles = ["Viewer", "Analyst", "Admin"]
    new_role = data.get("role").capitalize()

    if new_role not in valid_roles:
        return jsonify({"msg": "Invalid role"}), 400

    user.role = new_role
    db.session.commit()

    return jsonify({"msg": "Role updated"}), 200


# ===============================
# DELETE USER (FIXED 🔥)
# ===============================
@user_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@role_required(["admin"])
def delete_user(id):
    current_user_id = int(get_jwt_identity())

    # ❌ Prevent deleting yourself
    if current_user_id == id:
        return jsonify({"msg": "You cannot delete yourself"}), 400

    user = User.query.get(id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # 🔥 DELETE ALL RELATED TRANSACTIONS FIRST
    Transaction.query.filter_by(user_id=id).delete()

    # 🔥 DELETE USER
    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User and all transactions deleted"}), 200