from sqlalchemy import (
    Column, Integer, String, Boolean, Text, ForeignKey, DateTime,
    func, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from backend.app.core.database import init_db, BaseModel
from user import User
from agent import Agent


class Highlight(BaseModel):  # Characteristics: One user cannot highlight the same agent twice
    __tablename__ = "highlights"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="highlights")
    agent = relationship("Agent", back_populates="highlights")

    __table_args__ = (UniqueConstraint("user_id", "agent_id", name="_user_agent_highlight_uc"),)


init_db()