from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Shared properties
class GenerationBase(BaseModel):
    prompt: Optional[str] = Field(None, description="Prompt text")


# Properties to receive on creation (Internal use mostly, since API uses Form Data)
class GenerationCreate(GenerationBase):
    self_image_url: str
    target_image_url: Optional[str] = None


# Properties to return to the Frontend
class GenerationResponse(GenerationBase):
    id: int
    user_id: int
    self_image_url: str
    target_image_url: Optional[str] = None 
    generated_image_url: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    # Config to allow reading from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)
