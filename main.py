import telebot
import sqlite3
import random
from telebot import types
from sdamgia import SdamGIA

correct_answers = 0
count = 1
MAX_QUESTIONS = 3
MAX_UNANSWERED_QUESTIONS = 2
unanswered_questions = 0

sdamgia = SdamGIA()

bot = telebot.TeleBot('7043784416:AAHYJLZDPlqeSZkhC8hNGBKenEr6CISdgmQ')


def generate_math_question(a, b):  # a не может быть 0
    num1 = random.randint(a, b)
    num2 = random.randint(a, b)
    operator = random.choice(['+', '-', '*'])
    question = f"{num1} {operator} {num2}"
    return question


@bot.message_handler(commands=['start'])
def start(message):
    global question, correct_answers, count
    conn = sqlite3.connect('top_math.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), top varchar(50))')

    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Перед началом докажи, что ты не бот. \n'
                                      'Ответь на пару простых вопросов.')

    question = generate_math_question(1, 10)
    bot.send_message(message.chat.id, question)

    bot.register_next_step_handler(message, check_answer)


def check_answer(message):
    global question, correct_answers, count
    user_answer = message.text
    # Проверить, правильный ли ответ
    if eval(question) == int(user_answer):
        bot.send_message(message.chat.id, 'Правильно!')
        correct_answers += 1
    else:
        bot.send_message(message.chat.id, 'Неправильно.')
    # Отправить следующий вопрос
    if count < MAX_QUESTIONS:
        question = generate_math_question(1, 100)
        bot.send_message(message.chat.id, question)
        count += 1
        bot.register_next_step_handler(message, check_answer)
    else:
        bot.send_message(message.chat.id, 'Вы прошли проверку!')

        bot.send_message(message.chat.id,
                         f'Привет, {message.from_user.first_name}!\n'
                         f'Меня зовут mathbot. Я помогу тебе подготовится'
                         f' к ЕГЭ по математике', parse_mode='html')
        bot.send_message(message.chat.id,
                         f'{message.from_user.first_name}, выбери, чем ты хотел бы заняться сегодня: \n'
                         f'/test - проверь свои знания \n'
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


@bot.message_handler(commands=['repeat'])
def repeat(message):
    theorems = {
        1: "Теорема Пифагора: Квадрат длины гипотенузы равен сумме квадратов длин других двух сторон.",
        2: "Теорема синусов: Отношения сторон треугольника к синусам противолежащих углов равны",
        3: "Теорема косинусов: Квадрат стороны треугольника равен сумме квадратов двух других его сторон "
           "минус удвоенное произведение этих сторон, умноженное на косинус угла между ними"
    }

    theorem_number = random.randint(1, len(theorems))
    theorem_text = theorems[theorem_number]

    bot.send_message(message.from_user.id, theorem_text)
    bot.send_message(message.from_user.id, "Введите свой ответ:")
    bot.register_next_step_handler(message, check_theorem_answer)


def check_theorem_answer(message):
    pass

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
