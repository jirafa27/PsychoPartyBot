from datetime import datetime
from time import strftime

from models.database import SessionLocal
from models.meeting import Meeting
from models.user import User
from services.user_service import UserService


class MeetingService:
    def __init__(self):
        self.session = SessionLocal()

    def get_last_meeting_of_user(self, username: str):
        last_meeting_id = self.session.query(Meeting).join(User, Meeting.creator == User.id).filter(
            User.username == username).orderby(Meeting.id).first()
        return last_meeting_id

    def create_meeting(self, username: str):
        user_id = UserService().get_user_info(username=username)['id']
        new_meeting = Meeting(date=None, time=None, creator_id=user_id, title=None, description=None,
                              max_amount_of_participants=100)
        new_meeting = self.session.add(new_meeting)
        self.session.commit()
        return new_meeting

    def cancel_last_meeting_of_user(self, username):
        meeting = self.get_last_meeting_of_user(username=username)
        if meeting != None:
            self.session.delete(meeting)
            self.session.commit()

    def get_passed_meetings(self, username: str):
        now = datetime.now()
        passed_meetings = self.session.query(Meeting) \
            .join(User) \
            .filter(User.username == username) \
            .filter(strftime('%Y-%m-%d %H:%M', Meeting.date + ' ' + Meeting.time) < now.strftime('%Y-%m-%d %H:%M')) \
            .order_by(Meeting.id.desc()) \
            .all()

        return passed_meetings


    def get_participants_of_meeting(self, meeting_id: int):
        # Запрашиваем встречу и получаем всех участников
        meeting = self.session.query(Meeting).filter(Meeting.id == meeting_id).first()
        if meeting:
            return meeting.participants
        else:
            return []

    def set_date_of_meeting(self, date_of_meeting: str, username: str):
        last_meeting = self.get_last_meeting_of_user(username)
        if last_meeting:
            last_meeting.date = date_of_meeting
            self.session.commit()

    def set_time_of_meeting(self, time_of_meeting: str, username: str):
        last_meeting = self.get_last_meeting_of_user(username)
        if last_meeting:
            last_meeting.time = time_of_meeting
            self.session.commit()

    def set_title_of_meeting(self, title_of_meeting: str, username: str):
        last_meeting = self.get_last_meeting_of_user(username)
        if last_meeting:
            last_meeting.title = title_of_meeting
            self.session.commit()

    def set_description_of_meeting(self, description_of_meeting: str, username: str):
        last_meeting = self.get_last_meeting_of_user(username)
        if last_meeting:
            last_meeting.description = description_of_meeting
            self.session.commit()



