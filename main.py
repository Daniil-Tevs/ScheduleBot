import telebot
import datetime
from multiprocessing import *
from update_db import make_user, get_users_id
import time
import sqlite3
from telebot import types
from days_of_week import *

bot = telebot.TeleBot("5746856996:AAHKInwXo7Ka-HACHijMjooH2JER66cluJo")

connection = sqlite3.connect("user_data.db", check_same_thread=False)

BaseMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
whole_schedule_button = types.KeyboardButton("Полное расписание")
today_schedule_button = types.KeyboardButton("Сегодня")
tomorrow_schedule_button = types.KeyboardButton("Завтра")
BaseMarkup.add(whole_schedule_button,today_schedule_button,tomorrow_schedule_button)

def proc_start():
    p_to_start = Process(target=start_schedule)
    p_to_start.start()
    return p_to_start


def start_schedule():
    while True:
        users_id = get_users_id(connection)
        if users_id:
            if datetime.datetime.today().hour == 7:
                for i in users_id:
                    bot.send_message(i, "Доброе утро! Расписание на сегодня\n")
                    bot.send_message(i, choose_day(datetime.datetime.today().weekday()))
                time.sleep(60*60*24)


@bot.message_handler(commands=['start'])
def start_dialog(message):
    bot.send_message(message.chat.id,"Привет! Я телеграм-бот ScheduleBot, который пока помогает с учебным расписанием "
                                     "ПМИ 2 курса 3 подгруппе")
    bot.send_message(message.chat.id, "Выберете необходимое расписание", reply_markup=BaseMarkup)

    make_user(message.chat.id,"coming soon",connection)


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == "Полное расписание":
        with open("whole_schedule.png","rb") as image:
            bot.send_photo(message.chat.id,photo=image)
    elif message.text == "Сегодня":
        bot.send_message(message.chat.id,choose_day(datetime.datetime.today().weekday()), parse_mode="HTML")
    elif message.text == "Завтра":
        bot.send_message(message.chat.id,choose_day(datetime.datetime.today().weekday()+1), parse_mode="HTML")
    else:
        bot.send_message(message.chat.id,"Некорректная команда. Используйте /help")


if __name__ == '__main__':
    while True:
        pr = proc_start()
        try:
            bot.polling(none_stop=True)
        except Exception:
            pass
