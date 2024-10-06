from datetime import datetime

from models.database import Base, engine, SessionLocal
from models.user import User
from models.meeting import Meeting
from models.rating import Rating


def init_db():

    Base.metadata.create_all(bind=engine)


    print("Initialized the db")


if __name__ == "__main__":
    init_db()
    # Вставка данных в таблицу Meeting
    meeting1 = Meeting(id=1, date=datetime.strptime('24.12.1994', '%d.%m.%Y').date(),
                       time=datetime.strptime('23:34', '%H:%M').time(), title='esrfd', description='asdfd',
                       max_amount_of_participants=100)

    meeting2 = Meeting(id=2, date=datetime.strptime('24.12.1994', '%d.%m.%Y').date(),
                       time=datetime.strptime('23:00', '%H:%M').time(), title='aes', description='sdf',
                       max_amount_of_participants=50)

    # Вставка данных в таблицу User
    user1 = User(id=1, username='test', name='geesfd', age=23, active=1, description='sdfd')
    user2 = User(id=2, username='jirafa27', name='ква', age=29, active=1, description='пурус')

    # Вставка данных в таблицу Rating
    rating1 = Rating(id=1, rated_by_id=1, who_was_rated_id=2, score=4, comment='Хорошо',
                     date=datetime.strptime('24.12.1994', '%d.%m.%Y').date(), meeting_id=2)

    rating2 = Rating(id=2, rated_by_id=1, who_was_rated_id=2, score=5, comment='Отлично',
                     date=datetime.strptime('24.12.1994', '%d.%m.%Y').date(), meeting_id=1)

    # Добавление объектов в сессию
    session = SessionLocal()
    session.add(meeting1)
    session.add(meeting2)
    session.add(user1)
    session.add(user2)
    session.add(rating1)
    session.add(rating2)

    # Коммит транзакции для сохранения изменений
    session.commit()

    # Закрытие сессии
    session.close()