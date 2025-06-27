import pytest
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, Table, ForeignKey, DateTime,
    func, UniqueConstraint, CheckConstraint, create_engine
)
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import relationship, declarative_base


# Use SQLite in-memory DB for testing
Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


highlight_table = Table(
    "highlights", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("agent_id", Integer, ForeignKey("agents.id", ondelete="CASCADE")),
    UniqueConstraint("user_id", "agent_id", name="user_agent_highlight_uc")
)

# ----------------------
# Models
# ----------------------

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    # Use secondary table for highlights
    highlighted_agents = relationship(
        "Agent",
        secondary=highlight_table,
        back_populates="highlighted_by"
    )

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")


class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    homepage_url = Column(String)
    category = Column(String)
    source = Column(String)
    trending = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    highlighted_by = relationship(
        "User",
        secondary=highlight_table,
        back_populates="highlighted_agents"
    )

    reviews = relationship("Review", back_populates="agent", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="agent", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))
    content = Column(Text)

    user = relationship("User", back_populates="reviews")
    agent = relationship("Agent", back_populates="reviews")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))
    value = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    agent = relationship("Agent", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("user_id", "agent_id", name="user_agent_rating_uc"),
        CheckConstraint("value >= 1 AND value <= 5", name="rating_range_check")
    )

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_user_creation(db):
    user = User(username="alice", email="alice@example.com", hashed_password="hashed")
    db.add(user)
    db.commit()
    assert db.query(User).count() == 1
    assert db.query(User).first().username == "alice"

def test_agent_creation_and_query(db):
    agent = Agent(name="ChatGPT", category="Productivity")
    db.add(agent)
    db.commit()
    agent_from_db = db.query(Agent).filter_by(name="ChatGPT").first()
    assert agent_from_db is not None
    assert agent_from_db.category == "Productivity"

def test_user_highlight_many_agents(db):
    user = User(username="bob", email="bob@example.com", hashed_password="pw")
    a1 = Agent(name="Jasper", category="Marketing")
    a2 = Agent(name="CopyAI", category="Marketing")
    db.add_all([user, a1, a2])
    db.commit()
    user.highlighted_agents.extend([a1, a2])
    db.commit()
    assert len(user.highlighted_agents) == 2
    assert a1 in user.highlighted_agents
    assert user in a1.highlighted_by

def test_user_can_review_and_rate_agent(db):
    user = User(username="carl", email="carl@example.com", hashed_password="pw")
    agent = Agent(name="WriterAI", category="Education")
    db.add_all([user, agent])
    db.commit()
    review = Review(user_id=user.id, agent_id=agent.id, content="Helpful tool")
    rating = Rating(user_id=user.id, agent_id=agent.id, value=5)
    db.add_all([review, rating])
    db.commit()
    assert db.query(Review).count() == 1
    assert db.query(Rating).first().value == 5

def test_rating_constraint_violation(db):
    user = User(username="eve", email="eve@example.com", hashed_password="pw")
    agent = Agent(name="ToolX")
    db.add_all([user, agent])
    db.commit()
    with pytest.raises(Exception):
        bad_rating = Rating(user_id=user.id, agent_id=agent.id, value=6)  # invalid
        db.add(bad_rating)
        db.commit()

def test_highlight_uniqueness_constraint(db):
    user = User(username="dan", email="dan@example.com", hashed_password="pw")
    agent = Agent(name="ToolZ")
    db.add_all([user, agent])
    db.commit()
    insert1 = highlight_table.insert().values(user_id=user.id, agent_id=agent.id)
    insert2 = highlight_table.insert().values(user_id=user.id, agent_id=agent.id)
    db.execute(insert1)
    db.commit()
    with pytest.raises(Exception):
        db.execute(insert2)
        db.commit()