from models.database import SessionLocal
from models.meeting import Meeting
from models.user import User


class MeetingService:
    def __init__(self):
        self.session = SessionLocal()



    def get_last_meeting_id_of_user(self, username: str):
        last_meeting_id = self.session.query(Meeting.id).join(User, Meeting.creator==User.id).filter(User.username==username).one()
        return last_meeting_id

MeetingService().get_last_meeting_id_of_user("jirafa27")
