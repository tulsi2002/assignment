from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user_schema import UserCreate
from backend.utils.password_utlis import hash_password, verify_password

#  Create User
def create_user(db: Session, user_in : UserCreate):
    hashed_pw = hash_password(user_in.password)
    user = User(
        name = user_in.name,
        email = user_in.email,
        hashed_password = hashed_pw,
        role = user_in.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Authenticate User
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email== email).first()
    if not user:
        return None
    print("checking password:", password, "for user:", user.email)
    if not verify_password(password, user.hashed_password):
        print("Password check failed!")
        return None
    print("password check passed!")
    return user

# check if email already exists:
def get_user_by_email(db:Session, email: str):
    return db.query(User).filter(User.email== email).first()

# get user by id :
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()