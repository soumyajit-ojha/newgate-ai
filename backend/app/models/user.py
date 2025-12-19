from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User(Base):
    # __tablename__ is auto-generated as "users"

    email = Column(String(300), unique=True, index=True, nullable=False)
    google_id = Column(String(300), unique=True, index=True, nullable=False)
    full_name = Column(String(300), nullable=True)
    profile_picture = Column(String(300), nullable=True)

    # Modularity: Relationship to the generations table
    generations = relationship(
        "ImageGeneration", back_populates="owner", cascade="all, delete-orphan"
    )
