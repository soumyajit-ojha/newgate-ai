from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class ImageGeneration(Base):
    __tablename__ = "image_generations"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    input_image_url = Column(String, nullable=False)
    output_image_url = Column(String, nullable=True)
    status = Column(String, default="processing")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
