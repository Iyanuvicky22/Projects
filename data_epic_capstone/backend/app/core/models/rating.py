from sqlalchemy import (
    Column, Integer, String, Boolean, Text, ForeignKey, DateTime,
    func, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from backend.app.core.database import init_db, BaseModel
from user import User
from agent import Agent


class Rating(BaseModel):   # Characteristics: One user can only rate an agent once
    __tablename__ = "ratings"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))
    value = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    agent = relationship("Agent", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("user_id", "agent_id", name="_user_agent_rating_uc"),
        CheckConstraint("value >= 1 AND value <= 5", name="check_rating_range")
    )


init_db()