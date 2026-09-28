from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id         = Column(BigInteger, primary_key=True)
    problem_id = Column(BigInteger, ForeignKey("problems.id"), nullable=False)
    code       = Column(Text, nullable=False)
    language   = Column(Text, nullable=False)
    verdict    = Column(Text, default="QUEUED")
    created_at = Column(TIMESTAMP, server_default=func.now())

    problem = relationship("Problem", back_populates="submissions")