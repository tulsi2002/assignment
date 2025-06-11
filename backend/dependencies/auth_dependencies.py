from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader # it is a builtin fastapi class that tells fastapi to read APIkey from header.
from sqlalchemy.orm import Session
from backend.utils.jwt_utlis import decode_access_token
from backend.cruds.user_crud import get_user_by_id
from backend.db.session import get_db

# create an APIKeyHeader instance to extract value of Authorization header.
api_key_header = APIKeyHeader(name="Authorization")

# get current user from token:
def get_current_user_from_token(token: str= Security(api_key_header), db:Session= Depends(get_db)): # the extracted token will injected here.
    print("Received token:", token)
    try:
        if not token.startswith("Bearer"):
            raise HTTPException(status_code=401, detail="Invalid token format")
        token = token[len("Bearer "):] # remove bearer
        # decode the token
        payload = decode_access_token(token)
        user_id: int = payload.get("user_id")  # extract user_id and role from payload.
        role: str = payload.get("role")

        # check if payload is valid
        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        
        if role not in ["uploader", "admin"]:
            raise HTTPException(status_code=401, detail="Invalid Role")        
        # get user from database:
        user = get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception as e:
        print("error in decoding token:", e)
        raise HTTPException(status_code=401, detail= "Token is invalid or expired")
