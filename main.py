import telebot
import datetime
# from multiprocessing import *
import time
from update_db import make_user, get_users_id, get_group, delete_user
from telebot import types
from days_of_week import *

bot = telebot.TeleBot("5401716279:AAEbv4l-bgSxOEWV-IaaAlbj2FYMjPoUzDc")

BaseMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
whole_schedule_button = types.KeyboardButton("Полное расписание")
today_schedule_button = types.KeyboardButton("Сегодня")
tomorrow_schedule_button = types.KeyboardButton("Завтра")
whole_groups_button = types.KeyboardButton("Все группы")
webinar_list_button = types.KeyboardButton("Вебинар")
useful_links_button = types.KeyboardButton("Ссылки")
BaseMarkup.add(whole_schedule_button, today_schedule_button, tomorrow_schedule_button, whole_groups_button,
               webinar_list_button, useful_links_button)

'''def proc_start():
    p_to_start = Process(target=start_schedule, args=(id,))
    p_to_start.start()
    return p_to_start


def start_schedule(id):
    while True:
        users_id = get_users_id()
        if users_id:
            if datetime.datetime.today().hour == 7:
                for i in users_id:
                    bot.send_message(i, "Доброе утро! Расписание на сегодня\n")
                    bot.send_message(i, choose_day(datetime.datetime.today().weekday(), get_group(users_id)),
                                     parse_mode="HTML")
                time.sleep(60*60*23)
        time.sleep(60 * 50)

'''


def choose_group(message):
    if message.text.lower() == "первая":
        make_user(message.chat.id, "first")
        bot.send_message(message.chat.id, "Успешно! Выберете необходимое расписание", reply_markup=BaseMarkup)
    elif message.text.lower() == "вторая":
        make_user(message.chat.id, "second")
        bot.send_message(message.chat.id, "Успешно! Выберете необходимое расписание", reply_markup=BaseMarkup)
    elif message.text.lower() == "третья":
        make_user(message.chat.id, "third")
        bot.send_message(message.chat.id, "Успешно! Выберете необходимое расписание", reply_markup=BaseMarkup)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        one_button = types.KeyboardButton("Первая")
        two_button = types.KeyboardButton("Вторая")
        three_button = types.KeyboardButton("Третья")
        markup.add(one_button, two_button, three_button)
        bot.send_message(message.chat.id, "Неправильный выбор.Попробуйте ещё раз", reply_markup=markup)
        bot.register_next_step_handler(message, choose_group)


@bot.message_handler(commands=['start'])
def start_dialog(message):
    bot.send_message(message.chat.id, "Привет! Я телеграм-бот ScheduleBot, который пока помогает с учебным расписанием "
                                      "ПМИ 2 курса")
    delete_user(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    one_button = types.KeyboardButton("Первая")
    two_button = types.KeyboardButton("Вторая")
    three_button = types.KeyboardButton("Третья")
    markup.add(one_button, two_button, three_button)
    bot.send_message(message.chat.id, "Выберете подгруппу ПМИ 2 курса, в которой вы состоите", reply_markup=markup)

    bot.register_next_step_handler(message, choose_group)


def choose_answer(message):
    if message.text.lower() == "да":
        delete_user(message.chat.id)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        one_button = types.KeyboardButton("Первая")
        two_button = types.KeyboardButton("Вторая")
        three_button = types.KeyboardButton("Третья")
        markup.add(one_button, two_button, three_button)
        bot.send_message(message.chat.id, "Выберете подгруппу ПМИ 2 курса, в которую хотите перейти",
                         reply_markup=markup)
        bot.register_next_step_handler(message, choose_group)
    else:
        bot.send_message(message.chat.id, "Ваша группа осталась прежней", reply_markup=BaseMarkup)


@bot.message_handler(commands=['register'])
def register(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_btn = types.KeyboardButton("Да")
    no_btn = types.KeyboardButton("Нет")
    markup.add(yes_btn, no_btn)
    bot.send_message(message.chat.id, "Вы точно хотите выбрать другую группу?", reply_markup=markup)
    bot.register_next_step_handler(message, choose_answer)


@bot.message_handler(commands=['week'])
def send_whole_schedule(message):
    if get_group(message.chat.id) == "third":
        with open("whole_schedule.png", "rb") as image:
            bot.send_photo(message.chat.id, photo=image)
    elif get_group(message.chat.id) == "second":
        with open("whole_week_2.png", "rb") as image:
            bot.send_photo(message.chat.id, photo=image)
    elif get_group(message.chat.id) == "first":
        with open("whole_schedule.png", "rb") as image:
            bot.send_photo(message.chat.id, photo=image)


@bot.message_handler(commands=['today'])
def send_today_schedule(message):
    bot.send_message(message.chat.id,
                     choose_day(datetime.datetime.today().weekday(), get_group(message.chat.id)),
                     parse_mode="HTML")


@bot.message_handler(commands=['tomorrow'])
def send_tomorrow_schedule(message):
    bot.send_message(message.chat.id,
                     choose_day(datetime.datetime.today().weekday() + 1, get_group(message.chat.id)),
                     parse_mode="HTML")


@bot.message_handler(commands=['group'])
def send_groups_schedule(message):
    with open("2PM.pdf", "rb") as file:
        bot.send_document(message.chat.id, document=file)


@bot.message_handler(commands=['webinar'])
def send_webinar_list(message):
    bot.send_message(message.chat.id, "<b>Список вебинаров:</b>\n"
                                      "* Программированию микроконтроллеров:\n"
                                      "  - Лекция: https://events.webinar.ru/16703079/179657334\n"
                                      "  - Материалы: https://vk.me/join/AJQ1d3C88SKRApCmaOtJlQj6\n"
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


@bot.message_handler(commands=['youtube'])
def youtube(message):
    bot.send_message(message.chat.id, "<b>Список лекций на ютубе:</b>\n"
                                      "* МатЛогика 02.09\n"
                                      "  https://youtu.be/xWyiks6Ypo4"
                                      "* АЛиСД 02.09\n"
                                      "  https://youtu.be/WReuqUO7j_s\n"
                                      "* ОСиКС 02.09\n"
                                      "  https://youtu.be/_RLTvojQC0I\n"
                                      "* ПрМикроконтроллеров 07.09\n"
                                      "  https://youtu.be/2jodCu_yOvk\n"
                                      "* МатЛогика 09.09\n"
                                      "  https://youtu.be/Vofu08HI2Uk\n"
                                      "* АЛиСД 09.09\n"
                                      "  https://youtu.be/zT0kk99nOYw", parse_mode="HTML")


@bot.message_handler(commands=['links'])
def send_links_list(message):
    bot.send_message(message.chat.id, "<b>Список полезных ссылок:</b>\n"
                                      "* гугл диск бывшего 2-ого курса:\n"
                                      "  https://drive.google.com/drive/folders/1MYr-utIaiRHVbskXq2Pr52sGTZVlpECp\n"
                                      "* гугл диск Вероники Куртмулаевой(вся информация):"
                                      "  https://drive.google.com/drive/folders/1AU2O9guYIs3efC2zgT43ygU_kXaahefu\n"
                                      "* почта БФУ:\n"
                                      "  https://webmail.kantiana.ru/ (домен - students)\n"
                                      "* сайт физкультуры БФУ:\n"
                                      "  https://fc.kantiana.ru/\n"
                                      "* сайт личного кабинета БФУ:\n"
                                      "  https://lk.kantiana.ru/\n"
                     , parse_mode="HTML")
    bot.send_message(message.chat.id, "Чтобы получить список лекций в ютубе, пропишите /youtube", parse_mode="HTML")


@bot.message_handler(commands=['help'])
def help_user(message):
    bot.send_message(message.chat.id, "<b>Список моих команд:</b>\n"
                                      "* /week - расписание на всю неделю\n"
                                      "* /today - расписание на сегодня\n"
                                      "* /group - расписание для всех групп"
                                      "* /tomorrow - расписание на завтра\n"
                                      "* /webinar - список вебинаров\n"
                                      "* /register - сменить группу ПМИ\n"
                                      "* /links - полезные ссылки\n"
                                      "* /youtube - список лекций на YouTube\n", parse_mode="HTML")


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text.lower() == "привет" or message.text.lower() == "привет!":
        bot.send_message(message.chat.id, "Здравствуйте! Выберете необходимое действие", reply_markup=BaseMarkup)
    elif message.text.lower() == "как дела" or message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, "Очевидно, что у меня всё хорошо. Надеюсь у вас также! Выберете необходимое "
                                          "действие", reply_markup=BaseMarkup)
    elif message.text == "Полное расписание":
        send_whole_schedule(message)
    elif message.text == "Сегодня":
        send_today_schedule(message)
    elif message.text == "Завтра":
        send_tomorrow_schedule(message)
    elif message.text == "Вебинар":
        send_webinar_list(message)
    elif message.text == "Ссылки":
        send_links_list(message)
    elif message.text == "Все группы":
        send_groups_schedule(message)
    else:
        bot.send_message(message.chat.id, "Некорректная команда. Используйте /help")


if __name__ == '__main__':
    while True:
        # pr = proc_start()
        try:
            bot.polling(none_stop=True)
        except Exception:
            pass
