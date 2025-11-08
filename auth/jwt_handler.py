import os, time
import jwt
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "3600"))

def create_access_token(data: dict) -> str:
    payload = data.copy()
    now = int(time.time())
    payload.update({
        "iat": now,
        "exp": now + JWT_EXP_SECONDS
    })
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_access_token(token: str) -> dict:
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return data
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
