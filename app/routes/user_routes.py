from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Transaction
from app import db
from app.utils.decorators import role_required

user_bp = Blueprint("users", __name__)


# ===============================
# GET ALL USERS (Admin only)
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
# UPDATE USER ROLE (Admin only)
# ===============================
@user_bp.route("/<int:id>/role", methods=["PUT"])
@jwt_required()
@role_required(["admin"])
def update_role(id):
    data = request.get_json()

    if not data or "role" not in data:
        return jsonify({"msg": "Role is required"}), 400

    # FIX: normalize to lowercase to match how roles are stored in the DB
    new_role = data.get("role", "").strip().lower()

    if new_role not in ["viewer", "analyst", "admin"]:
        return jsonify({"msg": "Invalid role. Must be viewer, analyst, or admin"}), 400

    # FIX: use db.session.get() instead of deprecated Query.get()
    user = db.session.get(User, id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.role = new_role
    db.session.commit()

    return jsonify({"msg": "Role updated"}), 200


# ===============================
# DELETE USER (Admin only)
# ===============================
@user_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@role_required(["admin"])
def delete_user(id):
    current_user_id = int(get_jwt_identity())

    # Prevent admin from deleting themselves
    if current_user_id == id:
        return jsonify({"msg": "You cannot delete yourself"}), 400

    # FIX: use db.session.get() instead of deprecated Query.get()
    user = db.session.get(User, id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Delete all related transactions first (maintain referential integrity)
    Transaction.query.filter_by(user_id=id).delete()

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User and all transactions deleted"}), 200