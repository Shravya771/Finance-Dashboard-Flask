def validate_transaction(data):
    required_fields = ["amount", "type"]

    for field in required_fields:
        if field not in data:
            return False, f"{field} is required"

    if data["type"] not in ["income", "expense"]:
        return False, "Invalid type"

    return True, None



