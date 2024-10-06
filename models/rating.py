from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship
from models.database import Base

class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    rated_by_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    who_was_rated_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    score = Column(Integer, nullable=False, default=0)
    comment = Column(Text, nullable=False, default="")
    date = Column(String(10))
    meeting_id = Column(Integer, ForeignKey('meeting.id'))

    who_was_rated = relationship("User", foreign_keys=[who_was_rated_id], back_populates="received_ratings")
    rated_by = relationship("User", foreign_keys=[rated_by_id], back_populates="given_ratings")