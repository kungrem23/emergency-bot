import telebot
from telebot import types


jobs = {'systemAdmin': 'Сис. админ', 'cleaner': 'Уборщик', 'machineOperator': 'Станочник',
        'storekeeper': 'Кладовщик', 'director': 'Директор', 'electrician': 'Электрик', 'plumber': 'Сантехник',
        'security': 'Охранник', 'canteen': 'Сотрудник буфета', 'qualityControl': 'Контроль качества',
        'uchetchik': 'Учетчик', 'standardizer': 'Нормировщик', 'designEngineer': 'Инженер-конструктор',
        'processEngineer': 'Инженер-технолог', 'accountant': 'Бухгалтер', 'Лифтер': 'elevatorOperator',
        'Завхоз': 'supplyManager', 'other': 'Другое'}

markup_choose = types.InlineKeyboardMarkup(row_width=3)
# for i in jobs:
#     markup_choose.add(types.InlineKeyboardButton(jobs[i], callback_data=i + '_job'))
markup_choose.add(types.InlineKeyboardButton('Сис. админ', callback_data='systemAdmin_job'),
                  types.InlineKeyboardButton('Уборщик', callback_data='cleaner_job'),
                  types.InlineKeyboardButton('Станочник', callback_data='machineOperator_job'),
                  types.InlineKeyboardButton('Кладовщик', callback_data='storekeeper_job'),
                  types.InlineKeyboardButton('Директор', callback_data='director_job'),
                  types.InlineKeyboardButton('Электрик', callback_data='electrician_job'),
                  types.InlineKeyboardButton('Сантехник', callback_data='plumber_job'),
                  types.InlineKeyboardButton('Охранник', callback_data='security_job'),
                  types.InlineKeyboardButton('Сотрудник буфета', callback_data='canteen_job'),
                  types.InlineKeyboardButton('Контроль качества', callback_data='qualityControl_job'),
                  types.InlineKeyboardButton('Учетчик', callback_data='uchetchik_job'),
                  types.InlineKeyboardButton('Нормировщик', callback_data='standardizer_job'),
                  types.InlineKeyboardButton('Инженер-конструктор', callback_data='designEngineer_job'),
                  types.InlineKeyboardButton('Инженер-технолог', callback_data='processEngineer_job'),
                  types.InlineKeyboardButton('Бухгалтер', callback_data='accountant_job'),
                  types.InlineKeyboardButton('Лифтер', callback_data='elevatorOperator_job'),
                  types.InlineKeyboardButton('Завхоз', callback_data='supplyManager_job'),
                  types.InlineKeyboardButton('Другое', callback_data='other_job'))

markup_make_question = types.InlineKeyboardMarkup(row_width=3)
# for i in jobs:
#     markup_make_question.add(types.InlineKeyboardButton(jobs[i], callback_data=i + '_question'))
markup_make_question.add(types.InlineKeyboardButton('Сис. админ', callback_data='systemAdmin_question'),
                         types.InlineKeyboardButton('Уборщик', callback_data='cleaner_question'),
                         types.InlineKeyboardButton('Станочник', callback_data='machineOperator_question'),
                         types.InlineKeyboardButton('Кладовщик', callback_data='storekeeper_question'),
                         types.InlineKeyboardButton('Директор', callback_data='director_question'),
                         types.InlineKeyboardButton('Электрик', callback_data='electrician_question'),
                         types.InlineKeyboardButton('Сантехник', callback_data='plumber_question'),
                         types.InlineKeyboardButton('Охранник', callback_data='security_question'),
                         types.InlineKeyboardButton('Сотрудник буфета', callback_data='canteen_question'),
                         types.InlineKeyboardButton('Контроль качества', callback_data='qualityControl_question'),
                         types.InlineKeyboardButton('Учетчик', callback_data='uchetchik_question'),
                         types.InlineKeyboardButton('Нормировщик', callback_data='standardizer_question'),
                         types.InlineKeyboardButton('Инженер-конструктор', callback_data='designEngineer_question'),
                         types.InlineKeyboardButton('Инженер-технолог', callback_data='processEngineer_question'),
                         types.InlineKeyboardButton('Бухгалтер', callback_data='accountant_question'),
                         types.InlineKeyboardButton('Лифтер', callback_data='elevatorOperator_question'),
                         types.InlineKeyboardButton('Завхоз', callback_data='supplyManager_question'),
                         types.InlineKeyboardButton('Другое', callback_data='other_question')
                         )

markup_main = types.InlineKeyboardMarkup(row_width=2)
markup_main.add(types.InlineKeyboardButton('Просмотреть запросы', callback_data='questions'),
                types.InlineKeyboardButton('Создать запрос', callback_data='make_question'),
                types.InlineKeyboardButton('Стикеры', callback_data='stickers'),
                types.InlineKeyboardButton('Обучение', callback_data='learn'))

markup_main_director = types.InlineKeyboardMarkup(row_width=2)
markup_main_director.add(types.InlineKeyboardButton('Просмотреть запросы', callback_data='questions'),
                         types.InlineKeyboardButton('Создать запрос', callback_data='make_question'),
                         types.InlineKeyboardButton('Статистика', callback_data='stats'),
                         types.InlineKeyboardButton('Стикеры', callback_data='stickers'),
                         types.InlineKeyboardButton('Обучение', callback_data='learn'))

markup_question = types.InlineKeyboardMarkup(row_width=2)
markup_question.add(types.InlineKeyboardButton('Запросы для меня', callback_data='my_questions'),
                    types.InlineKeyboardButton('Все запросы', callback_data='all_questions'))

markup_to_main = types.InlineKeyboardMarkup(row_width=1)
markup_to_main.add(types.InlineKeyboardButton('Главное меню', callback_data='main_menu'))

markup_is_completed = types.InlineKeyboardMarkup(row_width=1)
markup_is_completed.add(types.InlineKeyboardButton('Решено', callback_data='completed'))

markup_level = types.InlineKeyboardMarkup(row_width=1)
markup_level.add(types.InlineKeyboardButton('🟢Может подождать🟢', callback_data='1_level'),
                 types.InlineKeyboardButton('🟡Выполнить как можно скорее🟡', callback_data='2_level'),
                 types.InlineKeyboardButton('🔴СРОЧНО исправить!🔴', callback_data='3_level'))

markup_stats = types.InlineKeyboardMarkup(row_width=1)
markup_stats.add(types.InlineKeyboardButton('Среднее кол-во добавленных задач в день', callback_data='avg_add_day'),
                 types.InlineKeyboardButton('Среднее кол-во выполненных задач в день', callback_data='avg_cmplt_day'),
                 types.InlineKeyboardButton('Средняя оценка выполнения задач', callback_data='avg_evaluation'),
                 types.InlineKeyboardButton('Главное меню', callback_data='main_menu'))

markup_back_stats = types.InlineKeyboardMarkup(row_width=1)
markup_back_stats.add(types.InlineKeyboardButton('Назад', callback_data='stats'))

markup_retry_director = types.InlineKeyboardMarkup(row_width=1)
markup_retry_director.add(types.InlineKeyboardButton('Назад', callback_data='login'),
                          types.InlineKeyboardButton('Попробовать снова', callback_data='director_job'))

markup_new_task = types.InlineKeyboardMarkup(row_width=1)
markup_new_task.add(types.InlineKeyboardButton('Решено', callback_data='completed'),
                    types.InlineKeyboardButton('Главное меню', callback_data='main_menu'))

markup_task_performance_evaluation = types.InlineKeyboardMarkup(row_width=5)
markup_task_performance_evaluation.add(types.InlineKeyboardButton('1', callback_data='1_performance'),
                                       types.InlineKeyboardButton('2', callback_data='2_performance'),
                                       types.InlineKeyboardButton('3', callback_data='3_performance'),
                                       types.InlineKeyboardButton('4', callback_data='4_performance'),
                                       types.InlineKeyboardButton('5', callback_data='5_performance'))

markup_back_to_main = types.InlineKeyboardMarkup(row_width=1)
markup_back_to_main.add(types.InlineKeyboardButton('Вернуться в главное меню', callback_data='main_menu'))

markup_learn = types.InlineKeyboardMarkup(row_width=1)
markup_learn.add(types.InlineKeyboardButton('Как создать запрос вручную', callback_data='2_learn'),
                 types.InlineKeyboardButton('Как создать запрос с помощью стикера', callback_data='3_learn'),
                 types.InlineKeyboardButton('Как просмотреть статистику', callback_data='4_learn'),
                 types.InlineKeyboardButton('Как ответить на запрос', callback_data='1_learn'),
                 types.InlineKeyboardButton('Вернуться', callback_data='main_menu'))

markup_back_learn = types.InlineKeyboardMarkup(row_width=1)
markup_back_learn.add(types.InlineKeyboardButton('Вернуться', callback_data='learn'))