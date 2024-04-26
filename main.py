import telebot
import sqlite3
from telebot import types
from sdamgia import SdamGIA


sdamgia = SdamGIA()


bot = telebot.TeleBot('6707527478:AAFR4BLfuoPCeQypsFgMfG2Zqu9cXpq_RKA')


@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.id)
    conn = sqlite3.connect('math_4.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (name int, top int)')
    conn = sqlite3.connect('top_math.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), top varchar(50))')

    conn.commit()
    cur.close()
    conn.close()


    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                      f'Меня зовут mathbot. Я помогу тебе пподготовится'
                                      f' к ЕГЭ по математике', parse_mode='html')

    bot.send_message(message.chat.id, f'Для начала введи команду /help, чтобы узнать о моих возможностях',
                     parse_mode='html')


DATA = []
K = 0
RES = [0, 0]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, выбери, чем ты хотел бы заняться сегодня: \n'
                                      f'/test - проверь свои знания \n'
                                      f'/rules - изучи новые для себя правила', parse_mode='html')


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


@bot.message_handler(commands=['test'])
def test(message):
    global DATA
    global K
    global RES

    K = 0

    bot.send_message(message.chat.id, f'Пройди небольшой тест и заработай баллы для рейтинга.'
                                      f'Вписывай ответы в формате экзамена.')

    subject = 'math'
    problems = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1}
    RES = [0, len(problems)]
    id = sdamgia.generate_test(subject, problems)
    data = sdamgia.get_test_by_id(subject, id)
    k = 0
    for id in data:
        k += 1
        bot.send_message(message.chat.id, f'№{k}')
        bot.send_message(message.chat.id, f'{sdamgia.get_problem_by_id(subject, id)["condition"]["text"]}')
        if sdamgia.get_problem_by_id(subject, id)["condition"]["images"]:
            bot.send_message(message.chat.id, f'Дополнительные материалы к заданию:')
            for i in sdamgia.get_problem_by_id(subject, id)["condition"]["images"]:
                bot.send_message(message.chat.id, i)
    DATA = data

    bot.send_message(message.chat.id, f'Вводи ответы последовательно. Числа с плавающей точкой  через запятую:')
    bot.register_next_step_handler(message, answer)


def reg(message):
    con = sqlite3.connect('math_4.sql')
    cur = con.cursor()
    data = cur.execute("""SELECT * FROM users""").fetchall()
    data = list(map(lambda x: x[0], data))
    print(data)
    con.close()
    if message.from_user.id not in data:
        print(1)
        conn = sqlite3.connect('math_4.sql')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users (name, top) VALUES ({message.from_user.id}, {0})')
        conn.commit()
        cur.close()
        conn.close()


def answer(message):
    global DATA
    global K
    global RES

    if K < len(DATA) and message.text.lower() != 'закончить тестирование':
        if message.text.replace(',', '.').isdigit() or message.text.replace(',', '').isdigit():
            subject = 'math'
            data = sdamgia.get_problem_by_id(subject, DATA[K])['answer']
            if message.text == data:
                bot.send_message(message.chat.id, f'Верно, ответ в задании №{K + 1} {data}')
                RES[0] += 1
            else:
                bot.send_message(message.chat.id, f'Неверно, ответ в задании №{K + 1} {data}')
            K += 1
            bot.register_next_step_handler(message, answer)
        else:
            bot.send_message(message.chat.id, f'Неверный формат ввода, попробуй ещё раз')
            bot.register_next_step_handler(message, answer)

    elif K >= len(DATA):
        bot.send_message(message.chat.id, f'Красавчик, твой результат {int(round(RES[0] / RES[1], 2) * 100)}%')
        conn = sqlite3.connect('math_4.sql')
        cur = conn.cursor()
        count = cur.execute(f'SELECT top FROM users '
                            f'WHERE name = {message.from_user.id}').fetchall()[0]
        count = list(count)[0]
        count += RES[0]
        cur.execute(f'UPDATE users '
                    f'SET top = {count} '
                    f'WHERE name = {message.from_user.id}')
        print(count)
        conn.commit()
        cur.close()
        conn.close()


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


bot.polling(none_stop=True)
