from telebot import types
import telebot
import sqlite3

bot = telebot.TeleBot('6707527478:AAFR4BLfuoPCeQypsFgMfG2Zqu9cXpq_RKA')


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('top_math.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass )')

    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                      f'Меня зовут mathbot. Я помогу тебе подготовится'
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
        img = open('4.jpg', 'rb')
        bot.send_chat_action(call.message.chat.id, 'upload_photo')  # сообщить пользователю о загрузке фото
        bot.send_photo(call.message.chat.id, img)  # отправить фото в чат
        img.close()  # закрыть файл


bot.polling(none_stop=True)
