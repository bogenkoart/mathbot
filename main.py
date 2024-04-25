import telebot
import sqlite3
from telebot import types
from sdamgia import SdamGIA


sdamgia = SdamGIA()


bot = telebot.TeleBot('6707527478:AAFR4BLfuoPCeQypsFgMfG2Zqu9cXpq_RKA')


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('top_math.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), top varchar(50))')

    conn.commit()
    cur.close()
    conn.close()

#    reg(message)

    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                      f'Меня зовут mathbot. Я помогу тебе пподготовится'
                                      f' к ЕГЭ по математике', parse_mode='html')

    bot.send_message(message.chat.id, f'Для начала введи команду /help, чтобы узнать о моих возможностях',
                     parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, выбери, чем ты хотел бы заняться сегодня: \n'
                                      f'/test - проверь свои знания \n'
                                      f'/repeat - повтори правила \n'
                                      f'/rules - изучи новые для себя правила \n'
                                      f'/workout - тренируй свои знания', parse_mode='html')


@bot.message_handler(commands=['rules'])
def key(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text='Алгебра', callback_data='b_1')
    item2 = types.InlineKeyboardButton(text='Геометрия', callback_data='b_2')
    markup.row(item1, item2)
    question = 'Выбери кнопку'
    bot.send_message(message.from_user.id, text=question, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('b'))
def callback_worker(call):
    if call.data == 'b_1':
        img_trig = open('trig.jpg', 'rb')
        bot.send_message(call.message.chat.id, 'Основные формулы в тригонометрии:')
        bot.send_photo(call.message.chat.id, img_trig)

        img_priv = open('priv.jpg', 'rb')
        bot.send_message(call.message.chat.id, 'Формулы приведения:')
        bot.send_photo(call.message.chat.id, img_priv)

        img_formulas = open('formulas.jpg', 'rb')
        bot.send_message(call.message.chat.id, 'Сокращенные формулы умножения:')
        bot.send_photo(call.message.chat.id, img_formulas)
    if call.data == 'b_2':
        img_plan = open('plan.png', 'rb')
        bot.send_message(call.message.chat.id, 'Основные правила планиметрии:')
        bot.send_photo(call.message.chat.id, img_plan)

        img_1_stereo = open('stereo.jpg', 'rb')
        img_2_stereo = open('stereo_1.jpg', 'rb')
        bot.send_message(call.message.chat.id, 'Основные правила стереометрии:')
        bot.send_photo(call.message.chat.id, img_1_stereo)
        bot.send_photo(call.message.chat.id, img_2_stereo)


# def reg(message):
#     conn = sqlite3.connect('top_math.sql')
#     cur = conn.cursor()
#
#     cur.execute(f'INSERT INTO users (name, pass) VALUES ({message.from_user.first_name}, {0})')
#
#     conn.commit()
#     cur.close()
#     conn.close()


bot.polling(none_stop=True)

