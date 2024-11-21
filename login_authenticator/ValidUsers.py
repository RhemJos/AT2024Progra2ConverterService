USERS = [
    {"username": "Admin", "password": "contraseña_123"},
    {"username": "User1", "password": "password_456"},
    {"username": "User2", "password": "securepass_789"}
]

def validate_user(username, password):
    #Validate if the username and password exist in USERS."""
    for user in USERS:
        if user["username"] == username and user["password"] == password:
            return True
    return False