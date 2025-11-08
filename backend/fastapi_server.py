"""
Merged FastAPI server with:
- existing /healthdata route
- /register and /login routes (auth merged into this file)
- simple protected route example

Notes:
- This file will try to use helper modules if you created them:
    auth.auth_service (hash_password, verify_password)
    auth.jwt_handler (create_access_token, decode_access_token)
    auth.roles (Role enum)
  If those modules are not found, this file will try to use local fallback
  implementations that require bcrypt and pyjwt to be installed.

- Recommended packages:
    pip install fastapi uvicorn bcrypt pyjwt python-dotenv pydantic

Run:
    uvicorn fastapi_server:app --reload
"""

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os

# Try to load dotenv if present (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Try to import helper modules (if you already created them in auth/)
# If not available, fall back to local implementations below.
USE_EXTERNAL_AUTH_MODULES = False
try:
    from auth.auth_service import hash_password, verify_password  # type: ignore
    from auth.jwt_handler import create_access_token, decode_access_token  # type: ignore
    from auth.roles import Role  # type: ignore
    USE_EXTERNAL_AUTH_MODULES = True
except Exception:
    USE_EXTERNAL_AUTH_MODULES = False

# Fallback simple implementations (require bcrypt + pyjwt)
if not USE_EXTERNAL_AUTH_MODULES:
    # Fallback: local simple implementations
    try:
        import bcrypt
        import jwt
        import time
    except Exception as e:
        raise RuntimeError(
            "Missing auth helper modules AND required packages. "
            "Install dependencies: pip install bcrypt pyjwt python-dotenv\n"
            "Or create auth/auth_service.py, auth/jwt_handler.py, auth/roles.py as instructed in your Week-4 roadmap."
        ) from e

    JWT_SECRET = os.getenv("JWT_SECRET", "change_this_secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "3600"))

    def hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
        except Exception:
            return False

    def create_access_token(data: Dict[str, Any]) -> str:
        payload = data.copy()
        now = int(time.time())
        payload.update({"iat": now, "exp": now + JWT_EXP_SECONDS})
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        # pyjwt >=2 returns str; older versions return bytes
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token

    def decode_access_token(token: str) -> Dict[str, Any]:
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return data
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    # Minimal Role enum fallback
    class Role(str):
        PATIENT = "patient"
        DOCTOR = "doctor"
        CAREGIVER = "caregiver"


# --- FastAPI app ---
app = FastAPI(title="Healthcare Monitoring Agent - Backend")

# --- Existing route you had: healthdata ---
@app.get("/healthdata")
def get_health_data():
    fitness_data = {
        "steps": 7500,
        "calories": 320,
        "heart_rate": 72,
        "sleep_hours": 7.5
    }
    return fitness_data


# --- Simple in-memory user store for initial testing ---
# Replace this with DB integration (SQLAlchemy / Session) in production.
users_db = []  # list of dicts: {"name","email","password","role"}


# --- Pydantic schemas ---
class RegisterIn(BaseModel):
    name: str
    email: str
    password: str
    role: str  # expects "patient"|"doctor"|"caregiver"


class LoginIn(BaseModel):
    email: str
    password: str


# --- Auth endpoints (register / login) ---
@app.post("/register")
def register(user: RegisterIn):
    # Validate role
    allowed_roles = {getattr(Role, "PATIENT"), getattr(Role, "DOCTOR"), getattr(Role, "CAREGIVER")}
    # allowed_roles may be attribute strings or class attributes; normalize:
    allowed_role_values = {r if isinstance(r, str) else r.value for r in allowed_roles}

    if user.role not in allowed_role_values:
        raise HTTPException(status_code=400, detail=f"Invalid role. Allowed: {allowed_role_values}")

    # check existing
    for u in users_db:
        if u["email"].lower() == user.email.lower():
            raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    new_user = {
        "name": user.name,
        "email": user.email.lower(),
        "password": hashed,
        "role": user.role
    }
    users_db.append(new_user)
    return {"message": "User registered successfully", "email": new_user["email"], "role": new_user["role"]}


@app.post("/login")
def login(payload: LoginIn):
    # simple lookup
    for u in users_db:
        if u["email"].lower() == payload.email.lower():
            if verify_password(payload.password, u["password"]):
                token = create_access_token({"email": u["email"], "role": u["role"]})
                return {"access_token": token, "token_type": "bearer", "role": u["role"]}
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")

    raise HTTPException(status_code=401, detail="Invalid credentials")


# --- Example protected route using Authorization: Bearer <token> header ---
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    else:
        token = authorization.strip()
    try:
        decoded = decode_access_token(token)
        return decoded
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.get("/protected")
def protected_route(current_user: dict = None, authorization: Optional[str] = Header(None)):
    # Using dependency manually to preserve simple signature (you can also use Depends)
    user = get_current_user(authorization)
    return {"message": "You have accessed a protected endpoint", "user": user}


# --- Small helper to seed a few users quickly (dev only) ---
@app.post("/seed-demo-users")
def seed_demo_users():
    # Only seed if empty
    if users_db:
        return {"message": "Users already seeded", "count": len(users_db)}
    demo = [
        ("Patient One", "patient@example.com", "patient123", getattr(Role, "PATIENT") if hasattr(Role, "PATIENT") else "patient"),
        ("Doctor One", "doctor@example.com", "doctor123", getattr(Role, "DOCTOR") if hasattr(Role, "DOCTOR") else "doctor"),
        ("Caregiver One", "caregiver@example.com", "caregiver123", getattr(Role, "CAREGIVER") if hasattr(Role, "CAREGIVER") else "caregiver"),
    ]
    for name, email, pwd, role in demo:
        users_db.append({"name": name, "email": email.lower(), "password": hash_password(pwd), "role": role})
    return {"message": "Seeded demo users", "count": len(users_db)}


# --- Notes for integration with real DB (replace this section later) ---
"""
Integration notes (do these when you replace the in-memory store):

- Replace `users_db` lookups with DB queries (SQLAlchemy session).
- Use a proper User model (id, name, email, password_hash, role).
- In register(), create + commit user row and return user id/email.
- In login(), query user by email and verify password against stored hash.
- For protected_route, fetch user from DB using user id in JWT (preferred) rather than only email.
- Use Alembic for database migrations to add a 'role' column if missing.

Example pattern (outline):
    from backend.db import SessionLocal
    from backend.models import User

    db = SessionLocal()
    user = db.query(User).filter(User.email == payload.email).first()
    if user and verify_password(...):
        token = create_access_token({"user_id": user.id, "email": user.email, "role": user.role})
"""

# End of file
