from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.user_schema import UserCreate, UserLogin
from backend.cruds.user_crud import create_user, authenticate_user, get_user_by_email
from backend.utils.jwt_utlis import create_access_token
from backend.db.session import get_db
from backend.utils.logger import logger

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


