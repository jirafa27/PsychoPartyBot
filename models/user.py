from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False, default="", unique=True)
    name = Column(String(32), nullable=False, default="")
    age = Column(Integer, nullable=True)
    active = Column(Integer, nullable=False, default=1)
    description = Column(String(5000), nullable=False, default="")

    given_ratings = relationship("Rating", foreign_keys="[Rating.rated_by_id]", back_populates="rated_by")
    received_ratings = relationship("Rating", foreign_keys="[Rating.who_was_rated_id]", back_populates="who_was_rated")
    meetings = relationship("Meeting", foreign_keys="[Meeting.id]", back_populates="creator")