import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ChatMemberUpdated, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder


from exceptions import DateIsLessThanTodayException, NoMeetingForCancelingException, TooLongStringException
from services.meeting_service import MeetingService
from services.user_service import UserService

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7202533150:AAHMwtAQi5JnsgEUNtGNwbBm9m1Q3HdTv80")
dp = Dispatcher()


class Mydialog(StatesGroup):
    name = State()
    age = State()
    description = State()
    error = State()
    main_menu = State()
    enter_date_of_meeting = State()
    enter_time_of_meeting = State()
    enter_title_of_meeting = State()
    enter_description_of_meeting = State()



@dp.message(lambda message: message.text.lower() == "главное меню" or message.text.lower() == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Мой профиль")],
        [types.KeyboardButton(text="Создать встречу")],
        [types.KeyboardButton(text="Найти встречу")],
        [types.KeyboardButton(text="Мои встречи")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    UserService().add_new_user(username=message.from_user.username, name=message.from_user.first_name)
    await state.set_state(Mydialog.main_menu)
    await message.answer(f"Привет, {message.from_user.first_name}!", reply_markup=keyboard)


@dp.message(F.text == "Создать встречу")
async def create_meeting(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Отменить создание встречи")],
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    MeetingService().create_meeting(message.from_user.username)
    await state.set_state(Mydialog.enter_date_of_meeting)
    await message.answer(f"Введите дату встречи в формате dd/mm/yyyy", reply_markup=keyboard)

@dp.message(F.text == "Отменить создание встречи")
@dp.message(F.text == "Удалить встречу")
async def cancel_meeting_creation(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Мой профиль")],
        [types.KeyboardButton(text="Создать встречу")],
        [types.KeyboardButton(text="Найти встречу")],
        [types.KeyboardButton(text="Мои встречи")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
    meeting = MeetingService().cancel_meeting(message.from_user.username)
    await state.set_state(Mydialog.main_menu)
    await message.answer(f"Встреча {meeting[0]} {meeting[1]} {meeting[2]} {meeting[4]} успешно отменена", reply_markup=keyboard)

@dp.message(F.text == "Мои встречи")
async def cancel_meeting_creation(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Мои прошедшие встречи")],
        [types.KeyboardButton(text="Мои запланированные встречи")],
        [types.KeyboardButton(text="Главное меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
    await message.answer(f"Выберите пункт меню", reply_markup=keyboard)


@dp.message(F.text == "Мои прошедшие встречи")
async def cancel_meeting_creation(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Главное меню")],
    ]
    builder = InlineKeyboardBuilder()
    passed_meetings = get_passed_meetings(message.from_user.username)
    await message.answer(f"Найдено {len(passed_meetings)} прошедших встреч")
    for meeting in passed_meetings:
        builder.add(types.InlineKeyboardButton(
            text="Оценить пользователей",
            callback_data="random_value")
        )

        await message.answer(
            f"Встреча {meeting[0]} Дата: {meeting[1]}\nВремя: {meeting[2]}\nНазвание: {meeting[4]}\nОписание: {meeting[5]}\n"
                 f"Cписок участников",
            reply_markup=builder.as_markup()
        )
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
    await message.answer(f"Выберите пункт меню", reply_markup=keyboard)

@dp.message(Mydialog.enter_date_of_meeting)
async def set_date_of_meeting(message: types.Message, state: FSMContext):
    date_of_meeting = message.text
    kb = [
        [types.KeyboardButton(text="Отменить создание встречи")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    format = "%d/%m/%Y"
    try:
        if datetime.strptime(date_of_meeting, format).date() < datetime.now().date():
            raise DateIsLessThanTodayException
        MeetingService().set_date_of_meeting(date_of_meeting, message.from_user.username)
        await state.set_state(Mydialog.enter_time_of_meeting)
        await message.answer(f"Введите время в формате hh:mm", reply_markup=keyboard)
    except ValueError:
        await state.set_state(Mydialog.enter_date_of_meeting)
        await message.answer(f"Неверный формат даты. Введите дату в формате dd/mm/yyyy", reply_markup=keyboard)
    except DateIsLessThanTodayException:
        await state.set_state(Mydialog.enter_date_of_meeting)
        await message.answer(f"Дата не может быть меньше текущей. Введите дату меньше текущей {datetime.now().date()} в формате dd/mm/yyyy", reply_markup=keyboard)

@dp.message(Mydialog.enter_time_of_meeting)
async def set_time_of_meeting(message: types.Message, state: FSMContext):
    time_of_meeting = message.text
    kb = [
        [types.KeyboardButton(text="Отменить создание встречи")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    format = "hh:mm"
    date_of_meeting = ""
    try:
        if not (0<=int(time_of_meeting.split(':')[0])<=23 and 0<=int(time_of_meeting.split(':')[0])<=59):
            raise ValueError
        date_of_meeting = get_date_of_last_user_meeting(message.from_user.username)
        datetime_format = "%d/%m/%Y %H:%M"
        if datetime.strptime(f"{date_of_meeting} {time_of_meeting}", datetime_format)<=datetime.now():
            raise DateIsLessThanTodayException
        set_time_of_meeting_db(time_of_meeting, message.from_user.username)
        await state.set_state(Mydialog.enter_title_of_meeting)
        await message.answer(f"Введите название встречи", reply_markup=keyboard)
    except ValueError as e:
        await state.set_state(Mydialog.enter_time_of_meeting)
        await message.answer(f"Неверный формат времени. Введите время в формате hh:mm. Время должно быть больше 00:00 и меньше 23:59", reply_markup=keyboard)
    except DateIsLessThanTodayException:
        await state.set_state(Mydialog.enter_time_of_meeting)
        await message.answer(f"Дата и время встречи {date_of_meeting} {time_of_meeting} раньше текущей даты и времени {datetime.now()}. Введите время позже текущего")


@dp.message(Mydialog.enter_title_of_meeting)
async def set_title_of_meeting(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Отменить создание встречи")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
    try:
        title_of_meeting = message.text
        if len(title_of_meeting) > 30:
            raise TooLongStringException
        set_title_of_meeting_db(title_of_meeting, message.from_user.username)
        await state.set_state(Mydialog.enter_description_of_meeting)
        await message.answer(f"Введите описание встречи", reply_markup=keyboard)
    except TooLongStringException:
        await state.set_state(Mydialog.enter_title_of_meeting)
        await message.answer(f"Название не должно превышать 30 символов", reply_markup=keyboard)



@dp.message(Mydialog.enter_description_of_meeting)
async def set_description_of_meeting(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Удалить встречу")],
        [types.KeyboardButton(text="Главное меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
    try:
        description_of_meeting = message.text
        if len(description_of_meeting) > 5000:
            raise TooLongStringException
        set_description_of_meeting_db(description_of_meeting, message.from_user.username)
        created_meeting = get_last_user_meeting(username=message.from_user.username)
        await message.answer(f"Встреча успешно создана\nДата: {created_meeting[1]}\nВремя: {created_meeting[2]}\nНазвание: {created_meeting[4]}\nОписание: {created_meeting[5]}", reply_markup=keyboard)
    except TooLongStringException:
        await state.set_state(Mydialog.enter_description_of_meeting)
        await message.answer(f"Описание не должно превышать 5000 символов", reply_markup=keyboard)


@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    delete_user(event.from_user.username)


@dp.message(F.text == "Мой профиль")
async def my_profile(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Обо мне")],
        [types.KeyboardButton(text="Мой рейтинг")],
        [types.KeyboardButton(text="Редактировать")],
        [types.KeyboardButton(text="Главное меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    await message.answer(f"Выберите пункт меню:", reply_markup=keyboard)


@dp.message(F.text == "Обо мне")
async def about_me(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Обо мне")],
        [types.KeyboardButton(text="Мой рейтинг")],
        [types.KeyboardButton(text="Редактировать")],
        [types.KeyboardButton(text="Главное меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    user_info = get_user_info(message.from_user.username)
    await message.answer(", ".join(map(str, user_info[0])), reply_markup=keyboard)



@dp.message(F.text == "Мой рейтинг")
async def my_rating(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Подробнее")],
        [types.KeyboardButton(text="Главное меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    rating = get_user_rating(message.from_user.username)
    await message.answer(f"Ваш рейтинг: {'Нет оценок' if rating==0 else rating}", reply_markup=keyboard)


@dp.message(F.text == "Подробнее")
async def my_rating_details(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Скачать все комментарии одним файлом")],
        [types.KeyboardButton(text="Главное меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    scores = get_user_rating_more_details(message.from_user.username)
    msg = ""
    for score in scores[:10]:
        msg+=f"Пользователь: {score[0]} \n Оценка: {score[1]} \n Комментарий: {score[2]}\n Дата: {score[3]}\n"
    await message.answer(f"Последние 10 комментариев:\n {'Нет оценок' if len(scores)==0 else msg}", reply_markup=keyboard)


@dp.message(F.text == "Скачать все комментарии одним файлом")
async def my_rating_details(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Главное меню")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    scores = get_user_rating_more_details(message.from_user.username)
    msg = ""
    for score in scores:
        msg += f"Пользователь: {score[0]} \n Оценка: {score[1]} \n Комментарий: {score[2]}\n Дата: {score[3]}\n"
    msg = "Нет комментариев" if len(msg) == 0 else f"Ваши комментарии:\n {msg}"
    text_file = BufferedInputFile(msg.encode("UTF-8"), filename="scores.txt")
    await message.answer_document(text_file)




@dp.message(F.text == "Редактировать")
async def edit_my_profile(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Редактировать имя")],
        [types.KeyboardButton(text="Редактировать возраст")],
        [types.KeyboardButton(text="Редактировать описание")],
        [types.KeyboardButton(text="Главное меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    await message.answer(f"Что редактируем?", reply_markup=keyboard)

@dp.message(F.text == "Редактировать имя")
async def edit_name(message: types.Message, state: FSMContext):
    await state.set_state(Mydialog.name)
    await message.answer(f"Введите новое имя")

@dp.message(F.text == "Редактировать возраст")
async def edit_age(message: types.Message, state: FSMContext):
    await state.set_state(Mydialog.age)
    await message.answer(f"Введите другой возраст")

@dp.message(F.text == "Редактировать описание")
async def edit_description(message: types.Message, state: FSMContext):
    await state.set_state(Mydialog.description)
    await message.answer(f"Введите другое описание")

@dp.message(Mydialog.name)
async def set_new_user_name(message: types.Message):
    new_name = message.text
    change_user_name(message.from_user.username, new_name)
    kb = [
        [types.KeyboardButton(text="Редактировать имя")],
        [types.KeyboardButton(text="Редактировать возраст")],
        [types.KeyboardButton(text="Редактировать описание")],
        [types.KeyboardButton(text="Главное меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    await message.answer(f"Успешно отредактировано. Что еще редактируем?", reply_markup=keyboard)

@dp.message(Mydialog.age)
@dp.message(Mydialog.error)
async def set_new_user_age(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Редактировать имя")],
        [types.KeyboardButton(text="Редактировать возраст")],
        [types.KeyboardButton(text="Редактировать описание")],
        [types.KeyboardButton(text="Главное меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
    try:
        new_age = int(message.text)
        change_user_age(message.from_user.username, new_age)
        await message.answer(f"Успешно отредактировано. Что еще редактируем?", reply_markup=keyboard)
    except ValueError:
        await message.answer(f"Ошибка. Введите число", reply_markup=keyboard)
        await state.set_state(Mydialog.error)

@dp.message(Mydialog.description)
async def set_new_user_description(message: types.Message):
    new_description = message.text
    change_user_description(message.from_user.username, new_description)
    kb = [
        [types.KeyboardButton(text="Редактировать имя")],
        [types.KeyboardButton(text="Редактировать возраст")],
        [types.KeyboardButton(text="Редактировать описание")],
        [types.KeyboardButton(text="Главное меню")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    await message.answer(f"Успешно отредактировано. Что еще редактируем?", reply_markup=keyboard)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())