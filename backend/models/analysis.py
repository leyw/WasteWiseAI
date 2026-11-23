from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    image_path = Column(String, nullable=False)
    waste_name = Column(String, nullable=True)
    category = Column(String, nullable=True)
    material = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    recommendation = Column(Text, nullable=True)   # JSON string
    is_mock = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="analyses")
