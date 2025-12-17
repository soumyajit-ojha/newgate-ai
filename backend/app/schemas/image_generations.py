from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Shared properties
class GenerationBase(BaseModel):
    prompt: str = Field(
        ..., min_length=3, description="Prompt must be at least 3 chars"
    )


# Properties to receive on creation (Internal use mostly, since API uses Form Data)
class GenerationCreate(GenerationBase):
    self_image_url: str
    target_image_url: str


# Properties to return to the Frontend
class GenerationResponse(GenerationBase):
    id: int
    user_id: int
    self_image_url: str
    target_image_url: str
    generated_image_url: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    # Config to allow reading from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)
