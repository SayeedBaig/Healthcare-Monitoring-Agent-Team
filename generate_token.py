from auth.jwt_handler import create_access_token

token = create_access_token({"email": "patient@example.com"})
print("Your JWT Token:\n")
print(token)