from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models import User

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)

            # ✅ FIX (case insensitive)
            if user.role.lower() not in [r.lower() for r in roles]:
                return jsonify({"msg": "Access denied"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper






