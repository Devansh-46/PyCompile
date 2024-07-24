# mytoken.py

class Token:
    def __init__(self, token_type, value):
        if not isinstance(token_type, str) or not isinstance(value, str):
            raise ValueError("Both token_type and value must be strings")
        self.type = token_type  # Add type attribute
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"
