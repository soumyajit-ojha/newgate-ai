from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base


# Enforce status types
class GenerationStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageGeneration(Base):
    # __tablename__ is auto-generated as "generations"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    prompt = Column(Text, nullable=False)

    self_image_url = Column(String(500), nullable=False)
    target_image_url = Column(String(500))

    generated_image_url = Column(String(500), nullable=True)

    # Status Tracking
    status = Column(String(100), default=GenerationStatus.PENDING, nullable=False)

    # Relationship back to User
    owner = relationship("User", back_populates="generations")
