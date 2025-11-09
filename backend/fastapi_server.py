# fastapi_server.py
"""
FastAPI server integrated with SQLite DB (uses health_data.db by default).
Features:
- /healthdata (existing)
- /register (stores user with role)
- /login (returns JWT)
- /protected (any authenticated user)
- /patient-only (requires role == "patient")
- /seed-demo-users (dev only; will create users only if they don't exist)

Run:
    uvicorn fastapi_server:app --reload --host 127.0.0.1 --port 8000
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any, Generator
import os

# dotenv (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# auth helper imports (use your auth/ files if present, otherwise fallback)
USE_EXTERNAL_AUTH_MODULES = False
try:
    from auth.auth_service import hash_password, verify_password  # type: ignore
    from auth.jwt_handler import create_access_token, decode_access_token  # type: ignore
    from auth.roles import Role  # type: ignore
    USE_EXTERNAL_AUTH_MODULES = True
except Exception:
    USE_EXTERNAL_AUTH_MODULES = False

if not USE_EXTERNAL_AUTH_MODULES:
    # fallback (requires pyjwt & bcrypt installed)
    import time
    import jwt
    import bcrypt

    JWT_SECRET = os.getenv("JWT_SECRET", "change_this_secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "3600"))

    def hash_password(plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

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
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token

    def decode_access_token(token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    class Role(str):
        PATIENT = "patient"
        DOCTOR = "doctor"
        CAREGIVER = "caregiver"

# --- FastAPI app ---
app = FastAPI(title="Healthcare Monitoring Agent - Backend")

# --- Existing healthdata route ---
@app.get("/healthdata")
def get_health_data():
    fitness_data = {
        "steps": 7500,
        "calories": 320,
        "heart_rate": 72,
        "sleep_hours": 7.5
    }
    return fitness_data

# --- Database setup (SQLAlchemy) ---
# Default DB file name: health_data.db (use DATABASE_URL in .env to override)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./health_data.db")

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User model (keeps parity with earlier roadmap)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="patient")

# Create tables if they don't exist (safe; won't drop existing data)
Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic schemas ---
class RegisterIn(BaseModel):
    name: str
    email: str
    password: str
    role: str

class LoginIn(BaseModel):
    email: str
    password: str

# --- Auth endpoints using DB ---
@app.post("/register")
def register(user: RegisterIn, db: Session = Depends(get_db)):
    allowed = {"patient", "doctor", "caregiver"}
    if user.role not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid role. Allowed: {allowed}")

    exists = db.query(User).filter(User.email == user.email.lower()).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    db_user = User(name=user.name, email=user.email.lower(), password_hash=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "email": db_user.email, "role": db_user.role}

@app.post("/login")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": user.id, "email": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role}

# --- Token helper ---
def get_current_user_from_header(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = authorization.split(" ", 1)[-1].strip()
    try:
        payload = decode_access_token(token)
        return payload
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# Protected generic route
@app.get("/protected")
def protected_route(current_user: Dict = Depends(get_current_user_from_header)):
    return {"message": "You have accessed a protected endpoint", "user": current_user}

# Role-protected example (patient only)
@app.get("/patient-only")
def patient_only(current_user: Dict = Depends(get_current_user_from_header)):
    if current_user.get("role") != "patient":
        raise HTTPException(status_code=403, detail="Forbidden: patient role required")
    return {"message": "Hello patient", "user": current_user}

# --- Dev helper: seed users if missing (will not overwrite existing users) ---
@app.post("/seed-demo-users")
def seed_demo_users(db: Session = Depends(get_db)):
    demo = [
        ("Patient One", "patient@example.com", "patient123", Role.PATIENT if hasattr(Role, "PATIENT") else "patient"),
        ("Doctor One", "doctor@example.com", "doctor123", Role.DOCTOR if hasattr(Role, "DOCTOR") else "doctor"),
        ("Caregiver One", "caregiver@example.com", "caregiver123", Role.CAREGIVER if hasattr(Role, "CAREGIVER") else "caregiver"),
    ]
    added = 0
    for name, email, pwd, role in demo:
        if not db.query(User).filter(User.email == email.lower()).first():
            db.add(User(name=name, email=email.lower(), password_hash=hash_password(pwd), role=role))
            added += 1
    if added:
        db.commit()
    return {"message": "Seed complete", "added": added}

# End of file
