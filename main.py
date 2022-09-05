import telebot
import datetime
from multiprocessing import *
from update_db import make_user, get_users_id
import time
import psycopg2
from telebot import types
from days_of_week import *

bot = telebot.TeleBot("5401716279:AAEbv4l-bgSxOEWV-IaaAlbj2FYMjPoUzDc")

connection = psycopg2.connect(
    database="da9ueqg4mqu8o1",
    user="rtijlvzrnnclrb",
    password="235899f24fffb504c10520411c96c7210782308ed71de37bfeed638043414ef4",
    host="ec2-99-81-16-126.eu-west-1.compute.amazonaws.com",
    port="5432"
)
cursor = connection.cursor()

BaseMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
whole_schedule_button = types.KeyboardButton("Полное расписание")
today_schedule_button = types.KeyboardButton("Сегодня")
tomorrow_schedule_button = types.KeyboardButton("Завтра")
webinar_list_button = types.KeyboardButton("Вебинар")
BaseMarkup.add(whole_schedule_button,today_schedule_button,tomorrow_schedule_button,webinar_list_button)

def proc_start():
    p_to_start = Process(target=start_schedule)
    p_to_start.start()
    return p_to_start


def start_schedule():
    while True:
        users_id = get_users_id(cursor)
        if users_id:
            if datetime.datetime.today().hour == 7:
                for i in users_id:
                    bot.send_message(i, "Доброе утро! Расписание на сегодня\n")
                    bot.send_message(i, choose_day(datetime.datetime.today().weekday()),parse_mode="HTML")
                time.sleep(60*60*24)
            else:
                time.sleep(60 * 60)


@bot.message_handler(commands=['start'])
def start_dialog(message):
    bot.send_message(message.chat.id,"Привет! Я телеграм-бот ScheduleBot, который пока помогает с учебным расписанием "
                                     "ПМИ 2 курса 3 подгруппе")
    bot.send_message(message.chat.id, "Выберете необходимое расписание", reply_markup=BaseMarkup)

    make_user(message.chat.id,"coming soon",cursor)
    connection.commit()


@bot.message_handler(commands=['week'])
def send_whole_schedule(message):
    with open("whole_schedule.png", "rb") as image:
        bot.send_photo(message.chat.id, photo=image)


@bot.message_handler(commands=['today'])
def send_today_schedule(message):
    bot.send_message(message.chat.id,choose_day(datetime.datetime.today().weekday()), parse_mode="HTML")


@bot.message_handler(commands=['tomorrow'])
def send_tomorrow_schedule(message):
    bot.send_message(message.chat.id,choose_day(datetime.datetime.today().weekday()+1), parse_mode="HTML")


@bot.message_handler(commands=['webinar'])
def send_webinar_list(message):
    bot.send_message(message.chat.id,"<b>Список вебинаров:</b>\n"
                                     "* Программированию микроконтроллеров: https://events.webinar.ru/16703079/179657334\n"
                                     "* Математическая логика:\n"
                                     "  - Материалы: https://t.me/+lUpBuovizpMwZGQy\n"
                                     "  - Лекция: https://events.webinar.ru/58904181/671873684\n"
                                     "* Алгоритмы и структуры данных: https://events.webinar.ru/58831439/1374164479\n"
                                     "* Операционным системам и компьютерным сетям:\n"
                                     "  - https://t.me/+5y8oyt6jVEBhYzBi\n"
                                     "  - https://events.webinar.ru/58858225/1592822786\n"
                                     "* Мат. Анализ:\n"
                                     "  - Материалы: https://cloud.mail.ru/public/52LR/55ceYr3fC\n"
                                     "  - Лекция: https://events.webinar.ru/58836733/956301003\n"
                                     "* Физра: Ещё нет (Вебинар)/Тесты в ЛМС", parse_mode="HTML")


@bot.message_handler(commands=['help'])
def help_user(message):
    bot.send_message(message.chat.id, "<b>Список моих команд:</b>\n"
                                      "* /week - расписание на всю неделю\n"
                                      "* /today - расписание на сегодня\n"
                                      "* /tomorrow - расписание на завтра\n"
                                      "* /webinar - список вебинаров", parse_mode="HTML")

@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == "Полное расписание":
        send_whole_schedule(message)
    elif message.text == "Сегодня":
        send_today_schedule(message)
    elif message.text == "Завтра":
        send_tomorrow_schedule(message)
    elif message.text == "Вебинар":
        send_webinar_list(message)
    else:
        bot.send_message(message.chat.id,"Некорректная команда. Используйте /help")


if __name__ == '__main__':
    while True:
        pr = proc_start()
        try:
            bot.polling(none_stop=True)
        except Exception:
            pass
