from telebot import types


jobs = {'systemAdmin': 'Сис. админ', 'cleaner': 'Уборщик', 'machineOperator': 'Станочник',
        'storekeeper': 'Кладовщик', 'director': 'Директор', 'electrician': 'Электрик', 'plumber': 'Сантехник',
        'security': 'Охранник', 'canteen': 'Сотрудник буфета', 'qualityControl': 'Контроль качества',
        'uchetchik': 'Учетчик', 'standardizer': 'Нормировщик', 'designEngineer': 'Инженер-конструктор',
        'processEngineer': 'Инженер-технолог', 'accountant': 'Бухгалтер', 'supplyManager': 'Завхоз',
        'elevatorOperator': 'Лифтер', 'other': 'Другое'}

markup_choose = types.InlineKeyboardMarkup(row_width=3)
for i in jobs:
    markup_choose.add(types.InlineKeyboardButton(jobs[i], callback_data=i + '_job'))

pass