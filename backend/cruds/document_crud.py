from sqlalchemy.orm import Session
from backend.models.document import Document
from backend.schemas.document_schema import DocumentOut
from backend.utils.logger import logger

# save document data to db
def save_document_metadata(db:Session, file_name: str, file_path: str,file_type: str, file_size: int, owner_id: int) -> Document:
    new_document = Document(
        file_name = file_name,
        file_path = file_path,
        file_type = file_type,
        file_size = file_size,
        owner_id = owner_id
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    logger.info(f"Document data saved : {new_document.file_name} (Owner ID: {owner_id})")
    return new_document

# Get document by user (Uploader) 
def get_document_by_user(db:Session, user_id: int, is_admin: bool = False):
    if is_admin:
        documents = db.query(Document).all()
        logger.info(f"Admin fetching all documents --> Count: {len(documents)}")
    else:
        documents = db.query(Document).filter(Document.owner_id == user_id).all()
        logger.info(f"User {user_id} fetching own documents → Count: {len(documents)}")    

    return documents    

# Get one document by ID:
def get_document_by_id(db:Session, document_id: int):
    document = db.query(Document).filter(Document.id==document_id).first()
    if document:
        logger.info(f"Document fetched --> ID: {document_id}")
    else: 
        logger.warning(f"Document not found → ID: {document_id}")
    return document