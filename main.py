import datetime
import telebot  # pip install pyTelegramBotAPI
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import token
from connect_db import connect_db
import db_functions

import re


faculty_data = ''
course_data = ''
group_data = ''
date_data = ''
subject_time_data = ''
subject_data = ''
cabinet_data = ''
teacher_data = ''

fteacher_name = ''
fteacher_data = ''
fdate_data = ''
fsubject_time_data = ''
fcabinet_data = ''
fsubject_data = ''
fgroup_data = ''


bot = telebot.TeleBot(token)


def gen_main_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Студент", callback_data="/student"), InlineKeyboardButton("Преподаватель", callback_data="/teacher"))
    return markup


@bot.message_handler(commands=['start', 'main_menu'])
def start_message(message):
    bot.send_message(message.chat.id, "Здравствуйте, выберите вашу роль", reply_markup=gen_main_markup()) # gen_main_markup


def find_teacher(message):
    global fteacher_name
    fteacher_name = '%'
    if message.text != '':
        msg = message.text
        fteacher_name = fteacher_name + msg
        fteacher_name = fteacher_name + '%'

    bot.send_message(message.chat.id, f"Результат поиска по запросу: {msg}", reply_markup=gen_fteacher_markup(message))
    teacher_count = get_fteacher_names()
    if len(teacher_count) == 0:
        new_markup = InlineKeyboardMarkup()
        new_markup.add(InlineKeyboardButton('⬅️ Вернуться к выбору роли', callback_data='other_role'))
        bot.send_message(message.chat.id, "По вашему запросу ничего не нашлось!", reply_markup=new_markup)



# ======================== Главное меню ==================
def get_faculty_names():
    faculty_names = []
    for i in db_functions.get_faculty_list():
        faculty_names.append(i[0])
    return faculty_names


def gen_faculty_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ Вернуться к выбору роли", callback_data="other_role"))
    for g in get_faculty_names():
        markup.add(InlineKeyboardButton(f' {g}', callback_data=g))
    return markup


def get_course_names():
    course_names = []
    for i in db_functions.get_current_faculty_courses_list(faculty_data):
        course_names.append(i[0])
    return course_names


def gen_course_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ Выбрать другой факультет", callback_data="other_faculty"))
    for g in get_course_names():
        markup.add(InlineKeyboardButton(f'💼 {g}', callback_data=g))
    return markup


def get_group_names():
    group_names = []
    for i in db_functions.get_current_course_groups_list(course_data, faculty_data):
        group_names.append(i[0])
    return group_names


def gen_group_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ Выбрать другой курс", callback_data="other_course"))
    for g in get_group_names():
        markup.add(InlineKeyboardButton(f'🎓 {g}', callback_data=g))
    return markup

def gen_teacher_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ Вернуться к выбору роли", callback_data="other_role"))
    return markup

def get_subject_names():
    subject_names = []
    for i in db_functions.get_current_subject_group_list(group_data, course_data):
        subject_names.append(i[0])
    return subject_names


def gen_subject_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ Выбрать другую группу", callback_data="other_group"))
    for g in get_subject_names():
        markup.add(InlineKeyboardButton(f'📚 {g}', callback_data=g))
    return markup


def get_date_names():
    date_names = []
    for i in db_functions.get_current_subject_date_list(subject_data, group_data):
        date_names.append(i[0])
    return date_names


def get_subject_time_names():
    subject_time_names = []
    for i in db_functions.get_current_subject_time_list(subject_data, group_data):
        subject_time_names.append(i[0])
    return subject_time_names


def get_cabinet_names():
    cabinet_names = []
    for i in db_functions.get_current_subject_cabinet_list(subject_data, group_data):
        cabinet_names.append(i[0])
    return cabinet_names


def get_teacher_names():
    teacher_names = []
    for i in db_functions.get_current_subject_teacher_list(subject_data, group_data):
        teacher_names.append(i[0])
    return teacher_names


def get_fteacher_names():
    faculty_names = []
    for i in db_functions.get_fteacher_list(fteacher_name):
        faculty_names.append(i[0])
    return faculty_names


def gen_fteacher_markup(message):
    markup = InlineKeyboardMarkup()
    for g in get_fteacher_names():
        markup.add(InlineKeyboardButton(f' {g}', callback_data=g))
    return markup

def get_fdate_names():
    date_names = []
    for i in db_functions.get_fdate_list(fteacher_data):
        date_names.append(i[0])
    return date_names

def get_fsubject_time_names():
    date_names = []
    for i in db_functions.get_ftime_list(fteacher_data):
        date_names.append(i[0])
    return date_names

def get_fcabinet_names():
    date_names = []
    for i in db_functions.get_fcabinet_list(fteacher_data):
        date_names.append(i[0])
    return date_names

def get_fsubject_names():
    date_names = []
    for i in db_functions.get_fsubject_list(fteacher_data):
        date_names.append(i[0])
    return date_names

def get_fgroup_names():
    date_names = []
    for i in db_functions.get_fgroup_list(fteacher_data):
        date_names.append(i[0])
    return date_names

# Обработчик нажатия на кнопки. Именно здесь заключена основная логика бота.
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global faculty_data
    global course_data
    global group_data #
    global date_data #
    global subject_time_data #
    global subject_data #
    global cabinet_data #
    global teacher_data #
    global fteacher_data
    global fdate_data
    global fsubject_time_data
    global fcabinet_data
    global fsubject_data
    global fgroup_data

    # Создаем меню выбора факультетов
    if call.data == '/student':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите ваш факультет!", reply_markup=gen_faculty_markup())

    elif call.data == '/teacher':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Напишите ФИО преподавателя:")
        bot.register_next_step_handler(msg, find_teacher)


# Создаем меню подтверждения добавления упражнения
    elif call.data == 'other_role':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите вашу роль!", reply_markup=gen_main_markup())

    elif call.data == 'other_faculty':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите ваш факультет!", reply_markup=gen_faculty_markup())

    elif call.data == 'other_course':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите ваш курс!", reply_markup=gen_course_markup())

    elif call.data == 'other_group':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите вашу группу!", reply_markup=gen_group_markup())

    elif call.data in get_faculty_names():
        faculty = call.data
        faculty_data = faculty
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выбран факультет: {faculty}\nВыберите курс.', reply_markup=gen_course_markup())

    elif call.data in get_course_names():
        course = call.data
        course_data = course
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выбран {course}\nВыберите группу.', reply_markup=gen_group_markup())

    elif call.data in get_group_names():
        group = call.data
        group_data = group
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выбрана группа: {group}\nВыберите предмет, чтобы посмотреть расписание интенсивов.', reply_markup=gen_subject_markup())

    elif call.data in get_fteacher_names():
        fteacher = call.data
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выбран преподаватель: {fteacher}')

        fteacher = call.data
        fteacher_data = fteacher
        fdate_data = get_fdate_names()
        fsubject_time_data = get_fsubject_time_names()
        fcabinet_data = get_fcabinet_names()
        fsubject_data = get_fsubject_names()
        fgroup_data = get_fgroup_names()
        curr_date = datetime.date.today()

        for i in range(len(fdate_data)):
            eto_data = fdate_data[i]
            date_time_obj = datetime.datetime.strptime(eto_data, '%Y-%m-%d').date()
            if date_time_obj < curr_date and date_time_obj != curr_date:
                db_functions.delete_old_schedule(eto_data)
            else:
                eto_time = fsubject_time_data[i]
                eto_cabinet = fcabinet_data[i]
                eto_subject = fsubject_data[i]
                eto_group = fgroup_data[i]
                bot.send_message(call.message.chat.id, f'📅 {eto_data}\n👥 {eto_group}\n⏰ {eto_time}\n📖 {eto_subject}\n🚪 {eto_cabinet}\n👨‍🔬 {fteacher}')
        bot.send_message(chat_id=call.message.chat.id, text=f'Расписание интенсивов преподавателя {fteacher} сформированы!', reply_markup=gen_teacher_markup())

    elif call.data in get_subject_names():
        subject = call.data
        subject_data = subject

        date_data = get_date_names()
        subject_time_data = get_subject_time_names()
        cabinet_data = get_cabinet_names()
        teacher_data = get_teacher_names()
        cur_date = datetime.date.today()
        for i in range(len(date_data)):
            eto_data = date_data[i]
            date_time_obj = datetime.datetime.strptime(eto_data, '%Y-%m-%d').date()
            if date_time_obj < cur_date and date_time_obj != cur_date:
                db_functions.delete_old_schedule(eto_data)
            else:
                eto_time = subject_time_data[i]
                eto_cabinet = cabinet_data[i]
                eto_teacher = teacher_data[i]
                bot.send_message(call.message.chat.id, f'📅 {eto_data}\n👥 {group_data}\n⏰ {eto_time}\n📖 {subject}\n🚪 {eto_cabinet}\n👨‍🔬 {eto_teacher}')



print('Bot in work....')
connect_db()
bot.polling(none_stop=True, interval=0)
