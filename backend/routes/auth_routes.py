from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user_schema import UserCreate, UserLogin, UpdatePasswordRequest
from backend.cruds.user_crud import create_user, authenticate_user, get_user_by_email
from backend.utils.jwt_utlis import create_access_token
from backend.db.session import get_db
from backend.utils.logger import logger
from backend.dependencies.auth_dependencies import get_current_user_from_token
from backend.utils.password_utlis import hash_password, verify_password

# create router
router = APIRouter()

# registration :
@router.post("/register",status_code=status.HTTP_201_CREATED)
def register(user_in:UserCreate, db:Session = Depends(get_db)):
    logger.info(f"Attempting to register user with email: {user_in.email}")
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        logger.warning(f"Email Already Exists-{user_in.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # checking password == confirm password
    if user_in.password != user_in.confirm_password:
        logger.warning(f"Password do not match for email: {user_in.email}")
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    allowed_roles = ["admin", "uploader"]
    if user_in.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Invalid Role")

    user = create_user(db, user_in)
    logger.info(f"User registered successfully: {user.email}")
    return {"message": "User registered successfully"}

# Login:
@router.post("/login")
def login(user_in:UserLogin, db:Session = Depends(get_db)):
    logger.info(f"login attempt for email: {user_in.email}")
    user = authenticate_user(db, user_in.email, user_in.password)
    if not user:
        logger.warning(f"Login failed for email: {user_in.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    # create JWT token
    access_token = create_access_token({
        "user_id": user.id,
        "role" : user.role
    })
    logger.info(f"User logged in successfully: {user.email}")

    return {
        "access_token": access_token,
        "token_type": "bearer"
        }

# Update password:
@router.put("/update-password")
def update_password(password_data: UpdatePasswordRequest, db:Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    logger.info(f"Password update attempt for user: {current_user.email}")
    # verifying password == current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        logger.warning(f"Incorrect current password for user {current_user.email}.")
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # check new_password == confirm new_password
    if password_data.new_password != password_data.confirm_new_password:
        logger.warning(f"Password confirmation does not match for user {current_user.email}.")
        raise HTTPException(status_code=400, detail="New passwords do not match")
    
    # update password
    current_user.hashed_password = hash_password(password_data.new_password)
    db.commit()
    logger.info(f"Password updated successfully for user {current_user.email}.")
    return {"message": "Password updated successfully"}

