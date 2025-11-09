
from backend.db import SessionLocal, init_db
from backend.models import Base, User
from auth.auth_service import hash_password

init_db(Base)
db = SessionLocal()
seed = [
    ("Patient One","patient@example.com","patient123","patient"),
    ("Doctor One","doctor@example.com","doctor123","doctor"),
    ("Caregiver One","caregiver@example.com","caregiver123","caregiver"),
]
for name,email,pwd,role in seed:
    if not db.query(User).filter(User.email==email).first():
        db.add(User(name=name,email=email,password_hash=hash_password(pwd),role=role))
db.commit()
db.close()
print("Seeded users")
