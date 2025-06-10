from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from backend.cruds import document_crud
from backend.models.user import User
from backend.schemas.document_schema import DocumentOut
from backend.utils.logger import logger
from backend.utils.encryption_utlis import encrypt_file, decrypt_file, fernet, encrypt_bytes
from backend.db.session import get_db
import os
import shutil
import uuid
from fastapi.responses import FileResponse
from backend.dependencies.auth_dependencies import get_current_user_from_token

router = APIRouter()

# Upload document:
@router.post("/upload",status_code=status.HTTP_201_CREATED)
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    #  read file content directly
    file_content = file.file.read()
    #  generate unique encrypted file name
    encrypted_file_name = f"{uuid.uuid4()}_{file.filename}.enc"
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    encrypted_file_path = os.path.join(upload_folder, encrypted_file_name)

    # encrypt and save encrypted file
    encrypt_bytes(file_content, encrypted_file_path)

    # save metadata in DB:
    new_document = document_crud.save_document_metadata(
        db=db,
        file_name=file.filename,
        file_path=encrypted_file_path,
        file_type=file.content_type,
        file_size=os.path.getsize(encrypted_file_path),
        owner_id=current_user.id
    )
    logger.info(f"Document uploaded successfully: {file.filename} by User {current_user.name}")
    return f"Document uploaded successfully: {file.filename} by User {current_user.name}"

# List documents
@router.get("/get_documents",response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    is_admin = current_user.role == "Admin"
    documents = document_crud.get_document_by_user(db=db, user_id=current_user.id, is_admin=(current_user.role.lower()=="admin"))
    logger.info(f"[LIST] User {current_user.id} ({current_user.role}) fetched documents → Count: {len(documents)}")

    return documents


# Document metadata
@router.get("/get_documents/{document}", response_model=DocumentOut)
def get_document_metadata(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    document = document_crud.get_document_by_id(db, document_id)
    if not document:
        logger.warning(f"[METADATA] Document not found → ID: {document_id}")
        raise HTTPException(status_code=404, detail="Document Not Found")
    
    if current_user.role.lower() != "admin" and document.owner_id != current_user.id:
        logger.warning(f"[METADATA] Access denied → User {current_user.id} tried to access document {document_id}")
        raise HTTPException(status_code=403, detail="Access denied")
    
    logger.info(f"[METADATA] Document metadata fetched --> ID: {document_id}")
    return document

# Download document
@router.get("/{document_id}/download")
def download_document(document_id: int, db: Session= Depends(get_db), current_user: User= Depends(get_current_user_from_token)):
    document = document_crud.get_document_by_id(db, document_id)
    if not document:
        logger.warning(f"[DOWNLOAD] Document not found → ID: {document_id}")
        raise HTTPException(status_code=404, detail="Document not found")
    if current_user.role.lower() != "admin" and document.owner_id != current_user.id:
        logger.warning(f"[DOWNLOAD] Access denied → User {current_user.id} tried to download document {document_id}")
        raise HTTPException(status_code=403, detail="Access denied")
    
    # decrypt file temporarily:
    decrypted_file_path = decrypt_file(document.file_path)
    logger.info(f"[DOWNLOAD] Document Downloaded: {document.file_name} -> Document ID: {document_id} -> By User {current_user.id}")

    # sent file to client
    return FileResponse(decrypted_file_path, media_type=document.file_type, filename=document.file_name)

        


