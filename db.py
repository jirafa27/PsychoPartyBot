import sqlite3

from exceptions import NoMeetingForCancelingException

conn = sqlite3.connect('data/db.db', check_same_thread=False)
cursor = conn.cursor()

# def add_new_user(username: str, name="", age=None, description=""):
#     try:
#         cursor.execute('INSERT INTO user (username, name, age, active, description) VALUES (?, ?, ?, ?, ?)',
#                         (username,  name, age, 1, description))
#         conn.commit()
#     except sqlite3.IntegrityError:
#         cursor.execute("UPDATE user SET active=1 WHERE username=?", (username,))
#         conn.commit()

# def delete_user(username: str):
#     cursor.execute(f"UPDATE user SET active=0 WHERE username=?", (username,))
#     conn.commit()


# def get_user_info(username: str):
#     cursor.execute(f"SELECT username, name, age, description FROM user WHERE user.username=?", (username,))
#     user_info = cursor.fetchall()
#     return user_info


# def get_user_rating(username: str):
#     cursor.execute(f"SELECT score FROM user JOIN rating ON user.id=rating.who_was_rated WHERE user.username=?",(username,))
#     user_rating = cursor.fetchall()
#     sum = 0
#     try:
#         for score in user_rating:
#             sum+=score[0]
#         rating = sum/len(user_rating)
#         print(rating)
#     except ZeroDivisionError:
#         return 0
#     return rating

# def get_user_rating_more_details(username: str):
#     cursor.execute(
#         "SELECT u2.username as rated_by, score, comment, rating.date FROM user as u1 JOIN rating ON u1.id=rating.who_was_rated JOIN user as u2 ON u2.id=rating.who_rated  WHERE u1.username=? ORDER BY date DESC", (username,))
#     user_rating_more_details = cursor.fetchall()
#     return user_rating_more_details

# def change_user_name(username: str, new_name: str):
#     cursor.execute("UPDATE user SET name=? WHERE username=?", (new_name, username))
#     conn.commit()

# def change_user_age(username: str, new_age: int):
#     cursor.execute("UPDATE user SET age=? WHERE username=?", (new_age, username))
#     conn.commit()
#
# def change_user_description(username: str, new_description: str):
#     cursor.execute("UPDATE user SET description=? WHERE username=?", (new_description, username))
#     conn.commit()

def get_last_meeting_id_of_user(username: str):
    print(username)
    cursor.execute("SELECT meeting.id FROM meeting JOIN user ON meeting.creator=user.id  WHERE user.username=? ORDER BY meeting.id DESC LIMIT 1", (username,))
    return cursor.fetchone()[0]


def create_meeting_in_db(username: str):
    cursor.execute('SELECT id FROM user WHERE username=?', (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute('INSERT INTO meeting (date, time, creator, title, description) VALUES (?, ?, ?, ?, ?)',
                   (None, None, user_id, None, None))
    conn.commit()

    last_meeting_id = get_last_meeting_id_of_user(username)

    cursor.execute("SELECT * FROM meeting WHERE id = ?", (last_meeting_id,))
    last_meeting = cursor.fetchone()

    cursor.execute('INSERT INTO user_meeting (user_id, meeting_id) VALUES (?, ?)',
                   (last_meeting[3], last_meeting[0]))
    conn.commit()



def cancel_meeting(username: str):
    cursor.execute('SELECT * FROM meeting JOIN user on meeting.creator=user.id WHERE user.username=? ORDER BY meeting.id DESC LIMIT 1', (username,))
    meeting_for_delete = cursor.fetchone()
    meeting_id_for_delete = meeting_for_delete[0]
    cursor.execute('DELETE FROM meeting WHERE meeting.id=? returning *',
                   (meeting_id_for_delete,))
    ans = cursor.fetchone()
    conn.commit()
    return ans

def get_passed_meetings(username: str):
    cursor.execute("SELECT * FROM meeting JOIN user on meeting.creator=user.id WHERE user.username=? AND DATETIME(meeting.date || ' ' || meeting.time) < DATETIME('now') ORDER BY meeting.id DESC", (username,))
    passed_meetings  = cursor.fetchall()
    return passed_meetings
def get_participants_of_meeting(meeting_id: int):
    cursor.execute("SELECT * FROM user_meeting JOIN user on meeting.id=user.id WHERE user.username=? AND DATETIME(meeting.date || ' ' || meeting.time) < DATETIME('now') ORDER BY meeting.id DESC", (username,))
    passed_meetings  = cursor.fetchall()
    return passed_meetings

def set_date_of_meeting_db(date_of_meeting: str, username: str):
    last_meeting_id = get_last_meeting_id_of_user(username)
    cursor.execute('UPDATE meeting SET date=? WHERE meeting.id=?', (date_of_meeting, last_meeting_id))
    conn.commit()


def set_time_of_meeting_db(time_of_meeting: str, username: str):
    last_meeting_id = get_last_meeting_id_of_user(username)
    cursor.execute('UPDATE meeting SET time=? WHERE meeting.id=?', (time_of_meeting, last_meeting_id))
    conn.commit()

def set_title_of_meeting_db(title_of_meeting: str, username: str):
    last_meeting_id = get_last_meeting_id_of_user(username)
    cursor.execute('UPDATE meeting SET title=? WHERE meeting.id=?', (title_of_meeting, last_meeting_id))
    conn.commit()


def set_description_of_meeting_db(description_of_meeting: str, username: str):
    last_meeting_id = get_last_meeting_id_of_user(username)
    cursor.execute('UPDATE meeting SET description=? WHERE meeting.id=?', (description_of_meeting, last_meeting_id))
    conn.commit()

def get_date_of_last_user_meeting(username: str):
    last_meeting_id = get_last_meeting_id_of_user(username)
    cursor.execute("SELECT meeting.date FROM meeting WHERE meeting.id=?", (last_meeting_id,))
    return cursor.fetchone()[0]

def get_last_user_meeting(username: str):
    last_meeting_id = get_last_meeting_id_of_user(username)
    cursor.execute("SELECT * FROM meeting WHERE meeting.id=?", (last_meeting_id,))
    return cursor.fetchone()
