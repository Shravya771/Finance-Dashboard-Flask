from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models import User
from app import db


def role_required(roles):
    """
    Decorator that restricts access to users whose role (stored lowercase)
    matches one of the allowed roles in the list.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())
            # FIX: use db.session.get() instead of deprecated Query.get()
            user = db.session.get(User, user_id)

            if not user:
                return jsonify({"msg": "User not found"}), 404

            # Roles in DB are lowercase; compare case-insensitively for safety
            if user.role.lower() not in [r.lower() for r in roles]:
                return jsonify({"msg": "Access denied"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper