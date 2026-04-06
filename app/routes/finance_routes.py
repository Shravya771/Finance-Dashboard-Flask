from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Transaction, User
from app.utils.decorators import role_required

finance_bp = Blueprint("finance", __name__)


def get_current_user():
    """Helper to fetch current user from JWT identity."""
    user_id = int(get_jwt_identity())
    return db.session.get(User, user_id)


# ===============================
# ADD TRANSACTION
# ===============================
@finance_bp.route("/", methods=["POST"])
@jwt_required()
def add_transaction():
    data = request.get_json()
    user_id = int(get_jwt_identity())

    amount = data.get("amount")
    type_ = data.get("type")

    if not amount or not type_:
        return jsonify({"msg": "Amount and type are required"}), 400

    if type_ not in ["income", "expense"]:
        return jsonify({"msg": "Type must be 'income' or 'expense'"}), 400

    new_transaction = Transaction(
        amount=amount,
        type=type_,
        category=data.get("category"),
        notes=data.get("notes"),
        user_id=user_id
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"msg": "Transaction saved"}), 201


# ===============================
# GET TRANSACTIONS
# ===============================
@finance_bp.route("/", methods=["GET"])
@jwt_required()
def get_transactions():
    user_id = int(get_jwt_identity())

    transactions = Transaction.query.filter_by(user_id=user_id).all()

    result = [{
        "id": t.id,
        "amount": t.amount,
        "type": t.type,
        "category": t.category,
        "notes": t.notes,
        "date": str(t.date)
    } for t in transactions]

    return jsonify({"transactions": result}), 200


# ===============================
# UPDATE TRANSACTION (Admin only)
# ===============================
@finance_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@role_required(["admin"])
def update_transaction(id):
    # FIX: use db.session.get() instead of deprecated Query.get()
    transaction = db.session.get(Transaction, id)

    if not transaction:
        return jsonify({"msg": "Transaction not found"}), 404

    # FIX: Admins can update ANY transaction (ownership check removed)
    # Non-admins cannot reach here due to @role_required(["admin"])

    data = request.get_json()
    transaction.amount = data.get("amount", transaction.amount)
    transaction.type = data.get("type", transaction.type)
    transaction.category = data.get("category", transaction.category)
    transaction.notes = data.get("notes", transaction.notes)

    db.session.commit()

    return jsonify({"msg": "Transaction updated"}), 200


# ===============================
# DELETE TRANSACTION (Admin only)
# ===============================
@finance_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@role_required(["admin"])
def delete_transaction(id):
    # FIX: use db.session.get() instead of deprecated Query.get()
    transaction = db.session.get(Transaction, id)

    if not transaction:
        return jsonify({"msg": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"msg": "Transaction deleted"}), 200


# ===============================
# SUMMARY
# ===============================
@finance_bp.route("/summary", methods=["GET"])
@jwt_required()
@role_required(["admin", "analyst", "viewer"])
def get_summary():
    user_id = int(get_jwt_identity())

    transactions = Transaction.query.filter_by(user_id=user_id).all()

    income = sum(t.amount for t in transactions if t.type == "income")
    expense = sum(t.amount for t in transactions if t.type == "expense")

    return jsonify({
        "income": income,
        "expense": expense,
        "balance": income - expense
    }), 200


# ===============================
# CATEGORY SUMMARY (Admin + Analyst)
# ===============================
@finance_bp.route("/category-summary", methods=["GET"])
@jwt_required()
@role_required(["admin", "analyst"])
def category_summary():
    user_id = int(get_jwt_identity())

    transactions = Transaction.query.filter_by(user_id=user_id).all()

    result = {}
    for t in transactions:
        if t.type == "expense":
            result[t.category] = result.get(t.category, 0) + t.amount

    return jsonify(result), 200


# ===============================
# FILTER TRANSACTIONS
# ===============================
@finance_bp.route("/filter", methods=["GET"])
@jwt_required()
def filter_transactions():
    user_id = int(get_jwt_identity())

    category = request.args.get("category")
    type_ = request.args.get("type")

    query = Transaction.query.filter_by(user_id=user_id)

    if category:
        query = query.filter_by(category=category)
    if type_:
        query = query.filter_by(type=type_)

    transactions = query.all()

    result = [{
        "id": t.id,
        "amount": t.amount,
        "type": t.type,
        "category": t.category,
        "notes": t.notes
    } for t in transactions]

    return jsonify(result), 200


# ===============================
# MONTHLY SUMMARY
# ===============================
@finance_bp.route("/monthly-summary", methods=["GET"])
@jwt_required()
def monthly_summary():
    user_id = int(get_jwt_identity())

    transactions = Transaction.query.filter_by(user_id=user_id).all()

    result = {}
    for t in transactions:
        month = t.date.strftime("%Y-%m")

        if month not in result:
            result[month] = {"income": 0, "expense": 0}

        if t.type == "income":
            result[month]["income"] += t.amount
        else:
            result[month]["expense"] += t.amount

    return jsonify(result), 200