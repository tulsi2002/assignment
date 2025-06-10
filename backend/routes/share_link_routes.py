from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.cruds import share_link_crud, document_crud
from backend.dependencies.auth_dependencies import get_current_user_from_token
from backend.schemas.share_link_schema import ShareLinkCreate, ShareLinkOut
from backend.db.session import get_db
from backend.utils.logger import logger
from backend.utils.encryption_utlis import decrypt_file
from fastapi.responses import FileResponse
from backend.models.user import User

router = APIRouter()

@router.post("/{document_id}/share/",response_model=ShareLinkOut)
def generate_share_link(
    document_id : int,
    share_link_in : ShareLinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)):
    # check if document exists
    document = document_crud.get_document_by_id(db, document_id)
    if not document:
        logger.warning(f"[SHARE] Document not found → ID: {document_id}")
        raise HTTPException(status_code=404, detail="Document not found")
    # check permission
    if current_user.role.lower() != "admin" and document.owner_id != current_user.id:
        logger.warning(f"[SHARE] Access denied → User {current_user.id} tried to share document {document_id}")
        raise HTTPException(status_code=403, detail="Access denied")
    
    # create share link
    share_link = share_link_crud.create_share_link(
        db=db,
        document_id=document_id,
        expiry_minutes=share_link_in.expiry_minutes,
        one_time=share_link_in.one_time
    )
    logger.info(f"[SHARE] Share link created → Document ID: {document_id} → Token: {share_link.token}")

    # return public link
    public_link = f"/public/{share_link.token}/download"
    return {
        "public_link": public_link,
        "expiry_time": share_link.expiry_time,
        "one_time": share_link.one_time,
        "accessed": share_link.accessed
    }


# Public download link:
@router.get("/public/{token}/download/")
def public_download(token: str, db: Session = Depends(get_db)):
    # get sharelink from database
    share_link = share_link_crud.get_share_link_by_token(db, token)
    if not share_link:
        logger.warning(f"[PUBLIC DOWNLOAD] Invalid token: {token}")
        raise HTTPException(status_code=404, detail="Invalid link")
    #  check link expiry;
    if share_link.expiry_time < datetime.utcnow():
        logger.warning(f"[PUBLIC DOWNLOAD] Link expired → Token: {token}")
        raise HTTPException(status_code=403, detail="Link has expired")
    # check one-time access use
    if share_link.one_time and share_link.accessed:
        logger.warning(f"[PUBLIC DOWNLOAD] One-time link already used → Token: {token}")
        raise HTTPException(status_code=403, detail="Link has already been used")
    # get document
    document = document_crud.get_document_by_id(db, share_link.document_id)
    if not document:
        logger.warning(f"[PUBLIC DOWNLOAD] Document not found → ID: {share_link.document_id}")
        raise HTTPException(status_code=404, detail="Document not found")
    # decrypt document
    decrypted_file_path = decrypt_file(document.file_path)
    logger.info(f"[PUBLIC DOWNLOAD] Document downloaded → Document ID: {document.id} → Token: {token}")

    # mark link as access:
    if share_link.one_time:
        share_link_crud.mark_share_link_as_accessed(db, share_link)

    # Return fileresponse:
    return FileResponse(
        decrypted_file_path,
        media_type=document.file_type,
        filename=document.file_name
    )





