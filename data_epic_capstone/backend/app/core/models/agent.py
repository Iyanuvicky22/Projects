from sqlalchemy import (
    Column, Integer, String, Boolean, Text, ForeignKey, DateTime,
    func, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from backend.app.core.database import init_db, BaseModel
from highlight import Highlight
from rating import Rating
from reveiw import Review


class Agent(BaseModel):  # Xteristics: Can be highlighted, reviewed, and rated by users. Can be marked trending (admin only)
    __tablename__ = "agents"

    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    homepage_url = Column(String)
    category = Column(String)
    source = Column(String)
    trending = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    highlights = relationship("Highlight", back_populates="agent", cascade="all, delete")
    reviews = relationship("Review", back_populates="agent", cascade="all, delete")
    ratings = relationship("Rating", back_populates="agent", cascade="all, delete")


init_db()