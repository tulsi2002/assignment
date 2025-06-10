from sqlalchemy.orm import Session
from backend.models.share_link import ShareLink
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"

# create share link 
def create_share_link(db:Session, document_id: int, expiry_minutes: int, one_time: bool ):
    # calculate the expiry time
    expiry_time = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    # payload for token
    payload = {
        "document_id": document_id,
        "exp": expiry_time,
        "one_time": one_time
    }
    # Generate JWT token
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    # save token in db so that we can see the one time usage of sharelink
    share_link = ShareLink(
        document_id=document_id,
        token=token,
        expiry_time=expiry_time,
        one_time=one_time,
        accessed=False
    )
    db.add(share_link)
    db.commit()
    db.refresh(share_link)

    return share_link 

# get share link by token ---> used in public
def get_share_link_by_token(db: Session, token: str):
    return db.query(ShareLink).filter(ShareLink.token == token).first()

# mark share link as accessed ---> used for one time .
def mark_share_link_as_accessed(db: Session, share_link: ShareLink):
    share_link.accessed = True
    db.commit()
    db.refresh(share_link)

# Decode share link token → used to validate token in public API
# used to ensure that token is valid or not.
def decode_share_link_token(token: str):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])    # extract payload
    return payload
