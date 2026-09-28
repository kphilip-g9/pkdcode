from sqlalchemy import Column, BigInteger, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Problem(Base):
    __tablename__ = "problems"

    id         = Column(BigInteger, primary_key=True)
    title      = Column(Text, nullable=False)
    statement  = Column(Text, nullable=False)
    difficulty = Column(Text)
    source     = Column(Text)
    source_url = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    test_cases  = relationship("TestCase",   back_populates="problem", cascade="all, delete")
    submissions = relationship("Submission", back_populates="problem")


class TestCase(Base):
    __tablename__ = "test_cases"

    id              = Column(BigInteger, primary_key=True)
    problem_id      = Column(BigInteger, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    input           = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_sample       = Column(Boolean, default=False)

    problem = relationship("Problem", back_populates="test_cases")