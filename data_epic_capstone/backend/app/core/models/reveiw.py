from sqlalchemy import (
    Column, Integer, String, Boolean, Text, ForeignKey, DateTime,
    func, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from backend.app.core.database import init_db, BaseModel
from user import User
from agent import Agent


class Review(BaseModel): # Characteristics: user writes a review for an agent
    __tablename__ = "reviews"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))
    content = Column(Text)

    user = relationship("User", back_populates="reviews")
    agent = relationship("Agent", back_populates="reviews")


init_db()