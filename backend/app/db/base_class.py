from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Base class for all models.
    Automatically adds ID and Time tracking to every table.
    """

    id = Column(Integer, primary_key=True, index=True)

    # Auto-set when created
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Auto-update when modified
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Helper to generate table name automatically from class name (User -> users)
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
