from models.database import SessionLocal
from models.rating import Rating
from models.user import User


class UserService:
    def __init__(self):
        self.session = SessionLocal()

    def add_new_user(self, username: str, name: str, age: int = None, description: str = ""):
        new_user = User(
            username=username,
            name=name,
            age=age,
            description=description
        )

        user = self.session.add(new_user)
        self.session.commit()
        return {"username": user.username, "name": user.name, "age": user.age, "description": user.description}

    def delete_user(self, username: str):
        user = self.session.query(User).filter(User.username==username).first()
        if user!=None:
            self.session.delete(user)
            self.session.commit()

    def get_user_info(self, username: str):
        user = self.session.query(User).filter(User.username==username).first()
        if user==None:
            return None
        self.session.refresh(user)
        return {"id": id, "username": user.username, "name": user.name, "age": user.age, "description": user.description}

    def get_user_rating(self, username: str):
        user_rating = (self.session.query(Rating.score)
                       .join(User, Rating.who_was_rated_id == User.id)
                       .filter(User.username == username).all())
        sum = 0
        try:
            for score in user_rating:
                sum += score[0]
            rating = sum / len(user_rating)
        except ZeroDivisionError:
            return 0
        return {"user_rating": rating}

    def get_user_rating_more_details(self, username: str):
        user_rating = (self.session.query(Rating)
                       .join(User, Rating.who_was_rated_id == User.id)
                       .filter(User.username == username).all())
        user_rating_details = []
        i = 0
        for rating in user_rating:
            user_rating_details.append({})
            user_rating_details[i]['rated_by'] = rating.rated_by.username
            user_rating_details[i]['score'] = rating.score
            user_rating_details[i]['comment'] = rating.comment
            user_rating_details[i]['date'] = rating.date
            i+=1
        return user_rating_details

    def change_username(self, old_username: str, new_username: str):
        user = self.session.query(User).filter(User.username == old_username).one()
        user.username = new_username
        self.session.commit()
        self.session.refresh(user)
        return {"username": user.username, "name": user.name, "age": user.age, "description": user.description}

    def change_user_age(self, username: str, new_age: int):
        user = self.session.query(User).filter(User.username == old_username).one()
        user.age = new_age
        self.session.commit()
        self.session.refresh(user)
        return {"username": user.username, "name": user.name, "age": user.age, "description": user.description}

    def change_user_description(self, username: str, new_description: str):
        user = self.session.query(User).filter(User.username == old_username).one()
        user.description = new_description
        self.session.commit()
        self.session.refresh(user)
        return {"username": user.username, "name": user.name, "age": user.age, "description": user.description}



print(UserService().change_username("jirafa27", "test"))
