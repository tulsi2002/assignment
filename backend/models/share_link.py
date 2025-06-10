from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.session import Base

class ShareLink(Base):
    __tablename__ = "share_links"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"),nullable=False)
    token = Column(String, unique=True, nullable=False)
    expiry_time = Column(DateTime, nullable=False)
    one_time = Column(Boolean, default=False)
    accessed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationship to documents:
    document = relationship("Document", backref="share_links")