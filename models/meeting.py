from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base


class Meeting(Base):
    __tablename__ = 'meeting'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(String(10))
    time = Column(String(5))
    creator_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    title = Column(String(30))
    description = Column(String(5000))
    max_amount_of_participants = Column(Integer)

    creator = relationship("User",  foreign_keys=[creator_id], back_populates="meetings")


