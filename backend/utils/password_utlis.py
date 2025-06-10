# this file is responsible for secure password handling.
# When a user registers → we never store raw password.
# We store hashed password → so that if DB is hacked, the passwords are not exposed.
# When a user logs in → we verify that their password matches the stored hashed password.

from passlib.context import CryptContext 
# passlib library is used for password hashing. 
# cryptcontext is a class that manages -- which hashing algo to used , how to hash pw and verify pw. 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# pwd_context is a object with tell to use bycrpt algo for pw hashing. 
# if we change algo in future then deprecated="auto" will upgrade the hashes. 

def hash_password(password: str)-> str :
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)-> bool: # used when user log in 
    return pwd_context.verify(plain_password, hashed_password)
