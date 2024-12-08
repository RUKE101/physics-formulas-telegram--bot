import telebot
from telebot import types
import time
import math

TOKEN = ''  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

# Создание объекта для хранения данных (для обработки поэтапных запросов)
user_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    go_to_main_menu(message)

# Обработчик выбора категории
@bot.message_handler(func=lambda message: message.text in ["МКТ", "Базовые задачи", "Термодинамика", "Цепи"])
def select_category(message):
    category = message.text
    if category == "МКТ":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("Давление газа")
        item2 = types.KeyboardButton("Средняя скорость молекул")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Выбери задачу из категории МКТ:", reply_markup=markup)
        user_data[message.chat.id] = {"category": "МКТ"}
    elif category == "Термодинамика":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("Работа газа")
        markup.add(item1)
        bot.send_message(message.chat.id, "Выбери задачу из категории Термодинамика:", reply_markup=markup)
        user_data[message.chat.id] = {"category": "Термодинамика"}
    elif category == "Цепи":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("Сила тока в цепи")
        markup.add(item1)
        bot.send_message(message.chat.id, "Выбери задачу из категории Цепи:", reply_markup=markup)
        user_data[message.chat.id] = {"category": "Цепи"}
# Обработчик категории
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "МКТ")
def mkt(message):
    if message.text.lower() == "давление газа":
        bot.send_message(message.chat.id, "Для расчета давления газа нужны следующие данные:\n"
                                           "1. Количество вещества газа (моль, n)\n"
                                           "2. Температура газа (в Kельвинах, T)\n"
                                           "3. Объем газа (м³, V)"
                                           "Введите все переменные подряд в формате без запятых. Пример: 2 4 6")
        user_data[message.chat.id] = {"task": "давление газа"}
    elif message.text.lower() == "средняя скорость молекул":
        bot.send_message(message.chat.id, "Для расчета средней скорости молекул нужны следующие данные:\n"
                                           "1. Температура газа (в Kельвинах, T)\n"
                                           "2. Масса одной молекулы газа (кг, m)"
                                           "Введите все переменные подряд в формате без запятых. Пример: 2 4")
        user_data[message.chat.id] = {"task": "средняя скорость молекул"}
# Обработчик категории
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "Термодинамика")
def thermodynamics(message):
    if message.text.lower() == "работа газа":
        bot.send_message(message.chat.id, "Для расчета работы газа нужны следующие данные:\n"
                                          "1. Давление газа (в Дж, P)\n"
                                          "2. Изменение объема газа (м³, ΔV)"
                                          "Введите все переменные подряд в формате без запятых. Пример: 2 4")
        user_data[message.chat.id] = {"task": "работа газа"}
# Обработчик категории
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("category") == "Цепи")
def chains(message):
    if message.text.lower() == "сила тока в цепи":
        bot.send_message(message.chat.id, "Для расчета силы тока в цепи нужны следующие данные:\n"
                                          "1. Напряжение (в Вольтах, В)\n"
                                          "2. Сопротивление в Омах, Ω)"
                                          "Введите все переменные подряд в формате без запятых. Пример: 2 4 6")
        user_data[message.chat.id] = {"task": "сила тока в цепи"}

# Обработчик формулы
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "давление газа")
def pressure(message):
    message_str = str(message.text)
    message_list = message_str.split()
    try:
        n = float(message_list[0])
        t = float(message_list[1])
        v = float(message_list[2])
        r = 8.314
        answer = (n * r * t) / v
        bot.send_message(message.chat.id, f'Ответом будет {answer}')
        go_to_main_menu(message)

    except:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")
        go_to_main_menu(message)

# Обработчик формулы
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "средняя скорость молекул")
def molecule_speed(message):
    message_str = str(message.text)
    message_list = message_str.split()
    try:
        t = float(message_list[0])
        m = float(message_list[1])
        k = 1.38e-23
        answer = math.sqrt((3 * k * t) / m)
        bot.send_message(message.chat.id, f'Ответом будет {answer}')
        go_to_main_menu(message)
    except:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")
        go_to_main_menu(message)

# Обработчик формулы
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "работа газа")
def gas_operation(message):
    message_str = str(message.text)
    message_list = message_str.split()
    try:
        p = float(message_list[0])
        delta_v = float(message_list[1])
        answer = p * delta_v
        bot.send_message(message.chat.id, f'Ответом будет {answer}')
        go_to_main_menu(message)
    except:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")
        go_to_main_menu(message)

# Обработчик формулы
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("task") == "сила тока в цепи")
def current_in_the_circuit(message):
    message_str = str(message.text)
    message_list = message_str.split()

    try:
        u = float(message_list[0])
        r = float(message_list[1])
        answer = u / r
        bot.send_message(message.chat.id, f'Ответом будет {answer}')
        go_to_main_menu(message)
    except:
        bot.send_message(message.chat.id, "Неверный формат данных, попробуйте снова.")
        go_to_main_menu(message)

# главное меню
def go_to_main_menu(message):
     markup=types.ReplyKeyboardMarkup(row_width=2)
     item1=types.KeyboardButton('МКТ')
     item2=types.KeyboardButton('Термодинамика')
     item3=types.KeyboardButton('Цепи')
     markup.add(item1,item2,item3)
     bot.send_message( message .chat .id ,'Выберите категорию:', reply_markup=markup)

if __name__ == '__main__':
   try:
       bot.infinity_polling()
   except Exception as e:
       print(f"Ошибка: {e}")
       time.sleep(5)
