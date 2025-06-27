from sqlalchemy import (
    Column, Integer, String, Boolean, Text, ForeignKey, DateTime,
    func, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from backend.app.core.database import init_db, BaseModel
from highlight import Highlight
from rating import Rating
from reveiw import Review


class User(BaseModel):   # Abilities: Can highlight, rate, and review agents
    __tablename__ = "users"

    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    highlights = relationship("Highlight", back_populates="user", cascade="all, delete")
    reviews = relationship("Review", back_populates="user", cascade="all, delete")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete")


init_db()