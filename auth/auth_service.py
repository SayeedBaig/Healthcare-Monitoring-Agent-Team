import bcrypt
from auth.jwt_handler import create_access_token

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def login_user(email: str, password: str):
    users = {
        "patient@gmail.com": {"password": "patient123", "role": "Patient"},
        "doctor@gmail.com": {"password": "doctor123", "role": "Doctor"},
        "caregiver@gmail.com": {"password": "care123", "role": "Caregiver"}
    }

    if email not in users or users[email]["password"] != password:
        raise Exception("Invalid email or password")

    token = create_access_token({
        "email": email,
        "role": users[email]["role"]
    })
    return token
