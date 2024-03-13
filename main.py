import datetime

import telebot
from telebot import types
from data import db_session
from data.markups import markup_choose, markup_main, markup_level, markup_question, markup_make_question, \
    markup_is_completed, markup_to_main, markup_main_director, markup_stats, markup_back_stats, markup_retry_director,\
    markup_new_task, markup_task_performance_evaluation, markup_back_to_main, markup_learn, markup_back_learn
from data.users import User
from data.questions import Question
from data.stickers import stickers_questions
import os

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

db_session.global_init("db/blogs.db")

jobs = {'systemAdmin': 'Сис. админ', 'cleaner': 'Уборщик', 'machineOperator': 'Станочник',
        'storekeeper': 'Кладовщик', 'director': 'Директор', 'electrician': 'Электрик', 'plumber': 'Сантехник',
        'security': 'Охранник', 'canteen': 'Сотрудник буфета', 'qualityControl': 'Контроль качества',
        'uchetchik': 'Учетчик', 'standardizer': 'Нормировщик', 'designEngineer': 'Инженер-конструктор',
        'processEngineer': 'Инженер-технолог', 'accountant': 'Бухгалтер', 'elevatorOperator': 'Лифтер',
        'supplyManager': 'Завхоз', 'other': 'Другое'}
videos_dict = {'1': 'Как ответить на запрос', '2': 'Как создать запрос вручную',
               '3': 'Как создать запрос с помощью стикера', '4': 'Как просмотреть статистику'}

users = dict()
password = '12345678'
check_director = []


def get_task_text(question):
    level = None
    if question.importance_level == 1:
        level = '🟢'
    elif question.importance_level == 2:
        level = '🟡'
    else:
        level = '🔴'
    text = 'id: ' + str(question.id) + '\n' + level * 5 + '\n' + \
           question.title  # + '\n' + question.content
    return text


def clear_states(id):
    users[id].set_head_state(False)
    users[id].set_content_state(False)
    users[id].set_job_q(None)
    users[id].set_image_state(False)


def add_question(datas, id):
    question = Question()
    # question.content = datas.get_content()
    question.title = datas.get_head()
    question.job = datas.get_job_q()
    question.image = datas.get_image()
    question.importance_level = datas.get_level()
    question.user_id = id
    db_sess = db_session.create_session()
    db_sess.add(question)
    db_sess.commit()
    return question


def get_question(id):
    db_sess = db_session.create_session()
    for question in db_sess.query(Question).filter(Question.id == id):
        return question


class UserState:
    def __init__(self):
        self.username = None
        self.user_id = None
        self.user_work = None
        self.head_q = None
        # self.text_q = None
        self.job_q = None
        self.image = None
        self.level = None
        self.is_sticker = False
        self.states = {'head': False, 'content': False, 'check_director': False, 'image': False}

    def get_username(self):
        return self.username

    def set_username(self, name):
        self.username = name

    def get_job(self):
        return self.user_work

    def get_head(self):
        return self.head_q

    # def get_content(self):
    #     return self.text_q

    def set_head(self, head):
        self.head_q = head

    # def set_content(self, content):
    #     self.text_q = content

    def set_id(self, idd):
        self.user_id = idd

    def set_job(self, job):
        self.user_work = job

    def set_job_q(self, job):
        self.job_q = job

    def get_job_q(self):
        return self.job_q

    def set_image(self, image):
        self.image = image

    def get_image(self):
        return self.image

    def set_level(self, level):
        self.level = level

    def get_level(self):
        return self.level

    def set_is_sticker(self, sticker):
        self.is_sticker = sticker

    def get_is_sticker(self):
        return self.is_sticker

    def set_head_state(self, state):
        self.states['head'] = state

    def set_content_state(self, state):
        self.states['content'] = state

    def set_director_state(self, state):
        self.states['check_director'] = state

    def set_image_state(self, state):
        self.states['image'] = state

    def get_states(self):
        return self.states


db_sess = db_session.create_session()
for user in db_sess.query(User):
    a = UserState()
    a.user_id = user.tg_id
    a.user_work = user.job
    users[user.tg_id] = a
    a.set_username(user.name)
db_sess.commit()
del db_sess


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in users.keys():
        clear_states(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    butt1 = types.InlineKeyboardButton('Войти', callback_data='login')
    markup.add(butt1)
    bot.send_message(message.chat.id, 'Elektron bot решает проблему мгновенного реагирования на бытовые проблемы внутри компании, например кофе пролили на лестнице или трубу прорвало. \nЕсли что-то произошло, вы можете оставить запрос стикерами бота или вручную, и бот оповестит об этом нужный персонал. Оповещая о проблеме, вы можете задавать ему уровень срочности: "не очень срочно", "как можно быстрее" или "решить прямо сейчас". Также вы сами можете следить за проблемам вашей компетенции и реагировать на них(устранять их) быстрее. Управляющий имеет возможность отслеживать статистику решаемости этих бытовых проблем относительно среднего количества поступающих и решённых и качества их устранения по оценкам тех, кто оставил запросы.')
    bot.send_message(message.chat.id, 'Привет, я ElektronBot. Я расскажу тебе о текущих проблемах на производстве',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'login':
                # db_session.global_init("db/blogs.db")
                db_sess = db_session.create_session()
                imin = False
                for user in db_sess.query(User).filter(User.tg_id == call.message.chat.id):
                    if call.message.chat.id not in users.keys():
                        uuser = UserState()
                        uuser.user_work = user.job
                        uuser.user_id = user.tg_id
                        uuser.set_username(user.name)
                        users[call.message.chat.id] = uuser
                    imin = True
                    if users[call.message.chat.id].get_job() == 'Директор':
                        if call.message.chat.id in users.keys():
                            bot.send_message(call.message.chat.id, 'Вы успешно вошли',
                                             reply_markup=markup_main_director)
                        else:
                            check_director.append(call.message.chat.id)
                            bot.send_message(call.message.chat.id, 'Введите пароль',
                                             reply_markup=markup_main_director)
                    else:
                        bot.send_message(call.message.chat.id, 'Вы успешно вошли', reply_markup=markup_main)
                    print('\t' + user.name + ' aka ' + user.tg_username + ' snova zapustil /start ')
                if imin is False:
                    bot.send_message(call.message.chat.id, 'Выберите должность', reply_markup=markup_choose)
                    print('\tkto-to vpervie zapustil /start')
                    # db_sess.add(user)
                db_sess.commit()
            # elif call.data == 'register':
            #     bot.send_message(call.message.chat.id, 'Введите ФИО')
            #     whereAmI = 'registerFIO'
            elif call.data == 'director_job':
                bot.send_message(call.message.chat.id, 'Введите пароль')
                check_director.append(call.message.chat.id)
                print('\t' + users[call.message.chat.id].get_username() + ' pitaetsa zayti pod direktorom')
            elif call.data[-4:] == '_job':
                job = jobs[call.data.split('_')[0]]
                db_sess = db_session.create_session()
                user = User()
                f_name = ''
                l_name = ''
                if call.message.chat.first_name is not None:
                    f_name = call.message.chat.first_name
                if call.message.chat.last_name is not None:
                    l_name = call.message.chat.last_name
                user.name = f_name + l_name
                user.tg_username = ''
                if call.message.chat.username is not None:
                    user.tg_username = call.message.chat.username
                user.tg_id = call.message.chat.id
                user.job = job
                db_sess.add(user)
                db_sess.commit()
                print('\t' + user.name + ' aka ' + user.tg_username + ' zaregalsya kak ', user.job)
                # if users[call.message.chat.id].get_job() == 'Директор':
                #     bot.send_message(call.message.chat.id, 'Вы успешно вошли', reply_markup=markup_main_director)
                # else:
                # if call.message.chat.id not in users.keys():
                uuser = UserState()
                uuser.user_work = user.job
                uuser.user_id = user.tg_id
                uuser.set_username(user.name)
                users[call.message.chat.id] = uuser
                bot.send_message(call.message.chat.id, 'Вы успешно вошли', reply_markup=markup_main)
                # uuser = UserState()
                # uuser.user_id = call.message.chat.id
                # uuser.user_work = job
                # users[call.message.chat.id] = uuser
            elif call.data == 'questions':
                bot.send_message(call.message.chat.id, 'Что вам интересно?', reply_markup=markup_question)
            elif call.data == 'my_questions':
                # db_session.global_init("db/blogs.db")
                db_sess = db_session.create_session()
                n = False
                for user in db_sess.query(User).filter(User.tg_id == call.message.chat.id):
                    for question in db_sess.query(Question).filter(Question.job == user.job): # and
                        if question.isCompleted == False:
                            n = True
                            # level = ''
                            # if question.importance_level == 1:
                            #     level = '🟢'
                            # elif question.importance_level == 2:
                            #     level = '🟡'
                            # else:
                            #     level = '🔴'
                            # text = 'id: ' + str(question.id) + '\n' + level * 5 + '\n' + \
                            #        question.title + '\n' + question.content
                            bot.send_photo(call.message.chat.id, question.image, caption=get_task_text(question),
                                           reply_markup=markup_is_completed)
                            # bot.send_message(call.message.chat.id, get_task_text(question),
                            # reply_markup=markup_is_completed)
                print('\t' + user.name + ' aka ' + user.tg_username + ' find questions for ' + user.job)
                if n:
                    bot.send_message(call.message.chat.id, 'Это все запросы на данный момент',
                                     reply_markup=markup_to_main)
                else:
                    bot.send_message(call.message.chat.id, 'Пока никто не создал запрос', reply_markup=markup_to_main)
                db_sess.commit()
            elif call.data == 'all_questions':
                db_sess = db_session.create_session()
                n = False
                for question in db_sess.query(Question).filter(Question.isCompleted == False):
                    n = True
                    # level = ''
                    # if question.importance_level == 1:
                    #     level = '🟢'
                    # elif question.importance_level == 2:
                    #     level = '🟡'
                    # else:
                    #     level = '🔴'
                    # text = 'id: ' + str(question.id) + '\n' + 'Роль: ' + question.job + '\n'\
                    #        + level * 5 + '\n' + question.title + '\n' + question.content + '\n\n' + \
                    #        question.created_date.strftime('%d.%m.%y %H:%M')
                    db_sess.commit()
                    bot.send_photo(call.message.chat.id, question.image, caption=get_task_text(question),
                                   reply_markup=markup_is_completed)
                    # bot.send_message(call.message.chat.id, get_task_text(question), reply_markup=markup_is_completed)
                for user in db_sess.query(User).filter(User.tg_id == call.message.chat.id):
                    print('\t' + user.name + ' aka ' + user.tg_username + ' find questions for everyone')
                if n:
                    bot.send_message(call.message.chat.id, 'Это все запросы на данный момент',
                                     reply_markup=markup_to_main)
                else:
                    bot.send_message(call.message.chat.id, 'Пока никто не создал запрос', reply_markup=markup_to_main)
            elif call.data == 'main_menu':
                # users[call.message.chat.id].set_head_state(False)
                # users[call.message.chat.id].set_content_state(False)
                # users[call.message.chat.id].set_job_q(False)
                clear_states(call.message.chat.id)
                if users[call.message.chat.id].get_job() == 'Директор':
                    bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=markup_main_director)
                else:
                    bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=markup_main)
                print('\t' + users[call.message.chat.id].get_username() + ' pereshel v main menu')
            elif call.data == 'make_question':
                bot.send_message(call.message.chat.id, 'Введите текст вопроса или выберите стикер',
                                 reply_markup=markup_back_to_main)
                users[call.message.chat.id].set_head_state(True)
                print('\t' + users[call.message.chat.id].get_username() + ' vvodit text voprosa')
            elif call.data[-9:] == '_question' and call.data != 'make_question':
                users[call.message.chat.id].set_job_q(jobs[call.data.split('_')[0]])
                bot.send_message(call.message.chat.id, 'Выберите уровень важности', reply_markup=markup_level)
                print('\t' + users[call.message.chat.id].get_username() + ' vibiraet uroven slozhnosti')
            elif call.data[-6:] == '_level':
                db_sess = db_session.create_session()
                users[call.message.chat.id].set_level(int(call.data.split('_')[0]))
                # question = add_question(users[call.message.chat.id], call.message.chat.id)
                question = Question()
                # question.content = users[call.message.chat.id].get_content()
                question.title = users[call.message.chat.id].get_head()
                question.job = users[call.message.chat.id].get_job_q()
                question.image = users[call.message.chat.id].get_image()
                question.importance_level = users[call.message.chat.id].get_level()
                question.user_id = call.message.chat.id
                db_sess = db_session.create_session()
                db_sess.add(question)
                db_sess.commit()
                # job = users[call.message.chat.id].get_job()
                # image = users[call.message.chat.id].get_image()
                # title = users[call.message.chat.id].get_head()
                # content = users[call.message.chat.id].get_content()
                users[call.message.chat.id].set_head(None)
                # users[call.message.chat.id].set_content(None)
                users[call.message.chat.id].set_job_q(None)
                users[call.message.chat.id].set_level(None)
                # question = Question()
                # question.title = users[call.message.chat.id].get_head()
                # question.content = users[call.message.chat.id].get_content()
                # question.job = users[call.message.chat.id].get_job_q()
                # question.importance_level = int(call.data.split('_')[0])
                # question.user_id = call.message.chat.id
                # question.image = users[call.message.chat.id].get_image()
                # db_sess.add(question)
                # db_sess.commit()
                bot.send_message(call.message.chat.id, 'Вы успешно создали запрос', reply_markup=markup_to_main)
                # level = ''
                # if question.importance_level == 1:
                #     level = '🟢'
                # elif question.importance_level == 2:
                #     level = '🟡'
                # else:
                #     level = '🔴'
                # text = 'id: ' + str(question.id) + '\n' + 'Роль: ' + question.job + '\n' \
                #        + level * 5 + '\n' + question.title + '\n' + question.content
                print('\t' + users[call.message.chat.id].get_username() + ' dobavil vopros')
                for user in db_sess.query(User).filter(User.job == question.job):
                    if user.tg_id == call.message.chat.id:
                        continue
                    try:
                        if user.tg_id == call.message.chat.id:
                            continue
                        # bot.send
                        bot.send_photo(user.tg_id,
                                       question.image,
                                       caption='Новая задача:' + '\n\n' +
                                               get_task_text(question),
                                       reply_markup=markup_new_task)
                        # bot.send_message(user.tg_id, 'Новая задача:' + '\n\n' + get_task_text(question),
                        # reply_markup=markup_new_task)
                        # users[user.tg_id].set_job_q(False)
                        # users[user.tg_id].set_head_state(False)
                        # users[user.tg_id].set_content_state(False)
                        clear_states(user.tg_id)
                    except Exception:
                        print(repr(Exception))
            elif call.data == 'completed':
                db_sess = db_session.create_session()
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                if call.message.html_caption.split('\n')[0] == 'Новая задача:':
                    id = call.message.html_caption.split('\n')[2].split(' ')[1]
                else:
                    id = call.message.html_caption.split('\n')[0].split(' ')[1]
                user_id = None
                for question in db_sess.query(Question).filter(Question.id == id):
                    question.isCompleted = True
                    if question.completed_date is None:
                        question.completed_date = datetime.datetime.now()
                    user_id = question.user_id
                    # question.timeDelta = question.completed_date - question.created_date
                db_sess.commit()
                if call.message.html_caption.split('\n')[0] == 'Новая задача:':
                    # bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=markup_to_main)
                    id_q = call.message.html_caption.split('\n')[2].split(' ')[1]
                    bot.send_photo(user_id,
                                   get_question(int(id_q)).image,
                                   caption='Пожалуйста, оцените качество выполнения задачи' + '\n\n' +
                                           get_task_text(get_question(int(id_q))),
                                   reply_markup=markup_task_performance_evaluation)
                try:
                    # bot.send_message(question.user_id, 'Пожалуйста, оцените качество выполнения задачи' + '\n\n' +
                    #                  get_task_text(question), reply_markup=markup_task_performance_evaluation)
                    id_q = call.message.html_caption.split('\n')[0].split(' ')[1]
                    bot.send_photo(user_id,
                                   get_question(int(id_q)).image,
                                   caption='Пожалуйста, оцените качество выполнения задачи' + '\n\n' +
                                           get_task_text(get_question(int(id_q))),
                                   reply_markup=markup_task_performance_evaluation)
                except Exception:
                    print(repr(Exception))
                print('\t' + users[call.message.chat.id].get_username() + ' vipolnil zadachu')
            elif call.data == 'stats':
                bot.send_message(call.message.chat.id, 'Что вам интересно?', reply_markup=markup_stats)
                print('\t' + users[call.message.chat.id].get_username() + ' vibiraet statistiku')
            elif call.data == 'avg_add_day':
                db_sess = db_session.create_session()
                days = dict()
                for question in db_sess.query(Question):
                    if question.created_date.date() in days.keys():
                        days[question.created_date.date()] += 1
                    else:
                        days[question.created_date.date()] = 1
                if len(days.values()) > 0:
                    count = sum(days.values()) / len(days.values())
                    bot.send_message(call.message.chat.id, 'В среднем добавлено задач в день ' + '%.2f' % count,
                                     reply_markup=markup_back_stats)
                else:
                    bot.send_message(call.message.chat.id, 'К сожалению, никто пока не добавил задачу',
                                     reply_markup=markup_back_stats)
                db_sess.commit()
                print('\t' + users[call.message.chat.id].get_username() + ' smotrit avg_add_day')
            elif call.data == 'avg_cmplt_day':
                db_sess = db_session.create_session()
                days = dict()
                for question in db_sess.query(Question):
                    if question.completed_date is not None:
                        if question.completed_date.date() in days.keys():
                            days[question.completed_date.date()] += 1
                        else:
                            days[question.completed_date.date()] = 1
                if len(days.values()) > 0:
                    count = sum(days.values()) / len(days.values())
                    bot.send_message(call.message.chat.id, 'В среднем выполнено задач в день ' + '%.2f' % count,
                                     reply_markup=markup_back_stats)
                else:
                    bot.send_message(call.message.chat.id, 'К сожалению, никто пока не выполнил задачи',
                                     reply_markup=markup_back_stats)
                db_sess.commit()
                print('\t' + users[call.message.chat.id].get_username() + ' smotrit avg_cmplt_day')
            elif call.data == 'avg_evaluation':
                db_sess = db_session.create_session()
                marks = []
                for question in db_sess.query(Question).filter(Question.task_performance_evaluation != None):
                    marks.append(question.task_performance_evaluation)
                if len(marks) > 0:
                    count = sum(marks) / len(marks)
                    bot.send_message(call.message.chat.id, 'Средняя оценка выполненных задач равна: ' + '%.2f' % count,
                                     reply_markup=markup_back_stats)
                else:
                    bot.send_message(call.message.chat.id,
                                     'К сожалению, никто пока не поставил оценку на выполнение задачи',
                                     reply_markup=markup_back_stats)
                db_sess.commit()
                print('\t' + users[call.message.chat.id].get_username() + ' smotrit avg_evaulation')
            elif call.data[1:] == '_performance':
                db_sess = db_session.create_session()
                for question in db_sess.query(Question).filter(Question.id ==
                                                               int(call.message.caption.split('\n')[2].split(' ')[1])):
                    question.task_performance_evaluation = int(call.data.split('_')[0])
                    db_sess.commit()
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id, 'Ваш отзыв очень важен для нас',
                                 reply_markup=markup_back_to_main)
                print('\t' + users[call.message.chat.id].get_username() + ' vibral performance')
            elif call.data == 'stickers':
                bot.send_message(call.message.chat.id, 'Стикеры бота:\nhttps://t.me/addstickers/electron_stickers',
                                 reply_markup=markup_back_to_main)
                print('\t' + users[call.message.chat.id].get_username() + ' smotrit stikeri')
            elif call.data == 'learn':
                bot.send_message(call.message.chat.id, 'Что вам интересно?', reply_markup=markup_learn)
                print('\t' + users[call.message.chat.id].get_username() + ' smotrit learn')
            elif call.data[-6:] == '_learn':
                video = open('videos/' + call.data.split('_')[0] + '.mp4', 'rb')
                bot.send_video(call.message.chat.id, video, timeout=15, reply_markup=markup_back_learn,
                               caption=videos_dict[call.data.split('_')[0]])
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=call.message.text, reply_markup=None)
            except Exception:
                try:
                    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             caption=call.message.caption, reply_markup=None)
                except Exception as ex:
                    print(repr(ex))

    except Exception as e:
        print(repr(e))


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.id in check_director:
        check_director.remove(message.chat.id)
        if message.text == password:
            bot.send_message(message.chat.id, 'Вы успешно вошли', reply_markup=markup_main_director)
            db_sess = db_session.create_session()
            user = User()
            f_name = ''
            l_name = ''
            if message.chat.first_name is not None:
                f_name = message.chat.first_name
            if message.chat.last_name is not None:
                l_name = message.chat.last_name
            user.name = f_name + l_name
            user.tg_username = ''
            if message.chat.username is not None:
                user.tg_username = message.chat.username
            user.tg_id = message.chat.id
            user.job = 'Директор'
            db_sess.add(user)
            db_sess.commit()
            uuser = UserState()
            uuser.user_id = message.chat.id
            for user in db_sess.query(User).filter(User.tg_id == message.chat.id):
                uuser.set_username(user.name)
            uuser.user_work = 'Директор'
            users[message.chat.id] = uuser
        else:
            bot.send_message(message.chat.id, 'Неверный пароль', reply_markup=markup_retry_director)
        print('\t' + users[message.chat.id].get_username() + ' vvel parol')
    elif users[message.chat.id].get_states()['head']:
        users[message.chat.id].set_head_state(False)
        # users[message.chat.id].set_content_state(True)
        users[message.chat.id].set_image_state(True)
        users[message.chat.id].set_head(message.text)
        # bot.send_message(message.chat.id, 'Введите содержимое вопроса', reply_markup=markup_back_to_main)
        bot.send_message(message.chat.id, 'Отправте фотографию проблемы(прнинимается только одна фотография)',
                         reply_markup=markup_back_to_main)
        print('\t' + users[message.chat.id].get_username() + ' vvel head')
    elif users[message.chat.id].get_states()['content']:
        # users[message.chat.id].set_content_state(False)
        users[message.chat.id].set_image_state(True)
        # users[message.chat.id].set_content(message.text)
        bot.send_message(message.chat.id, 'Отправте фотографию проблемы(прнинимается только одна фотография)',
                         reply_markup=markup_back_to_main)
        print('\t' + users[message.chat.id].get_username() + ' vvel content')
    # bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
    # text=message.text, reply_markup=None)
# db_session.global_init("db/blogs.db")
# db_sess = db_session.create_session()
# user = User()
# user.name = 'Данил'
# user.tg_username = 'kungrem23'
# user.job = 'директор'
# db_sess.add(user)
# db_sess.commit()
# a = db_sess.query(User).filter(User.tg_username == 'bebra')
# for user in a:
#     if user.name == '':
#         print('pusto')
#     else:
#         print(user.name)

# @bot.message_handler(content_types=['text'])
# def log_in(message):
#     if message.text == 'Войти':
#         bot.send_message(message.chat.id, 'Введите код сотрудника')
#
#
# @bot.message_handler(content_types=['text'])
# def register(message):
#     if message.text == 'Регистрация':
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         bot.send_message(message.chat.id, 'Введите ФИО', reply_markup=markup)


@bot.message_handler(content_types=['sticker'])
def sticker_answer(message):
    if users[message.chat.id].get_states()['head']:
        if message.sticker.file_unique_id in stickers_questions.keys():
            question = stickers_questions[message.sticker.file_unique_id]
            # question.user_id = message.chat.id
            # question.created_date = datetime.datetime.now()
            # db_sess = db_session.create_session()
            # db_sess.add(question)
            # db_sess.commit()
            users[message.chat.id].set_head(question.title)
            # users[message.chat.id].set_content(question.content)
            users[message.chat.id].set_level(question.importance_level)
            users[message.chat.id].set_job_q(question.job)
            users[message.chat.id].set_head_state(False)
            users[message.chat.id].set_image_state(True)
            users[message.chat.id].set_is_sticker(True)
            bot.send_message(message.chat.id, 'Скиньте фотографию проблемы', reply_markup=markup_back_to_main)
            print('\t' + users[message.chat.id].get_username() + ' skinul pravilniy stiker')

        else:
            users[message.chat.id].set_head_state(True)
            bot.send_message(message.chat.id,
                             'Неизвестный стикер. Попробуйте еще раз. Введите заголовок или выберите стикер',
                             reply_markup=markup_back_to_main)
            print(message.sticker.file_unique_id)
            print('\t' + users[message.chat.id].get_username() + ' skinul nepravilniy stiker')

@bot.message_handler(content_types=['photo'])
def image_answer(message):
    if users[message.chat.id].get_states()['image']:
        users[message.chat.id].set_image_state(False)
        file_info = bot.get_file(message.photo[-1].file_id)
        download = bot.download_file(file_info.file_path)
        users[message.chat.id].set_image(download)
        # bot.send_message(message.chat.id, '')
        # with open('images/images.jpg', 'wb') as new_image:
        #     new_image.write(download)
        # with open('images/images.jpg', 'rb') as new_image:
        #     bot.send_photo(message.chat.id, new_image)
        print('\t' + users[message.chat.id].get_username() + ' skinul photo')
        if users[message.chat.id].get_is_sticker():
            add_question(users[message.chat.id], message.chat.id)
            users[message.chat.id].set_is_sticker(False)
            bot.send_message(message.chat.id, 'Вы успешно создали запрос', reply_markup=markup_to_main)
            print('\t' + users[message.chat.id].get_username() + ' sozdal vopros s pomoshyu stikera')
        else:
            bot.send_message(message.chat.id, 'Выберите человека, который должен решить проблему',
                             reply_markup=markup_make_question)


bot.polling(none_stop=True)
