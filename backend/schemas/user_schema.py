from pydantic import BaseModel, EmailStr

# used for user registration
class UserCreate(BaseModel):
    name : str
    email : EmailStr
    password : str
    confirm_password : str
    role : str = "Uploader"

# used for user login
class UserLogin(BaseModel):
    email : EmailStr
    password : str

# response 
class UserResponse(BaseModel):
    id : int
    name : str
    email : EmailStr
    role : str