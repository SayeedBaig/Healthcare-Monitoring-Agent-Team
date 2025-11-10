import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth.auth_service import login_user
from auth.jwt_handler import decode_access_token

print("=== Manual Authentication Test ===\n")

# ✅ Successful login
try:
    token = login_user("patient@gmail.com", "patient123")
    print("✅ Login success, token created:", token[:40], "...\n")
except Exception as e:
    print("❌ Login failed:", e, "\n")

# 🚫 Invalid login
try:
    login_user("wrong@gmail.com", "wrongpass")
except Exception as e:
    print("✅ Invalid login blocked:", e, "\n")

# 🧠 Token validation
token = login_user("doctor@gmail.com", "doctor123")
decoded = decode_access_token(token)
print(f"✅ Token decoded successfully for: {decoded['email']} | Role: {decoded['role']}\n")

print("=== All manual tests completed successfully ===")
