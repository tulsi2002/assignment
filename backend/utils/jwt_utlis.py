# used to handle JWT Token creation and decoding.
'''
1. create_access_token() --> to generate JWT Token.
2. decode_access_token() --> used later when we want to validate token
'''
# jose.jwt is a python library that support jwt creation and decoding . work well with fastapi .
from jose import jwt  
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta  # used to set token expiration time

# load enviornment variable
load_dotenv()

# Read JWT_SECRET_KEY from .env
# secret key generate signature on the token.--> make sure token can not be modified . 
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256" # standard and secure signing algo. 

# Token expiration time (example: 1 hour)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Function to create JWT token
#  This function is called when user logs in successfully.
def create_access_token(data: dict): # take data in dictionary 
    to_encode = data.copy() # make a copy of data so that original data can not be modified, add expiration data to copy data.
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # Calculate expiration time for the token (60 mins)
    to_encode.update({"exp": expire}) # add expiration to dict data , exp is JWT class that tell token when to expire.
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM) # jwt.encode encode the data and sign the token.
    return encoded_jwt

# Function to decode JWT token
# used to verify the token wheaher it is valid or not, decode the data (get the data inside).
def decode_access_token(token: str): # func take the token.
    # print("decoding_token:", token)
    decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]) 
    # jwt.decode verify token using secret_key and check expiration time , and then decode the data. 
    # if token is expire or invalid it will raise the JWTError or ExpiredSignatureError. 
    return decoded_token
