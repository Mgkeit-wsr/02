import telebot
from telebot import types
bot = telebot.TeleBot('5126469852:AAF-TEF0Hbo8yq5hWgivlNhYYKqt64GQCms')

f = open('DataBase.txt', 'r', encoding='UTF-8')
lines = [*map(lambda x: x.strip(), f.readlines())]

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global price
    global score
    if call.data == "collage":
        collage(call.message)
    elif call.data == "VUZ":
        bot.send_message(person, 'Раздел в разработке')
        bot.send_message(person, 'Возвращаю в главное меню')
        bot.register_next_step_handler(call.message, start)
    elif call.data == "yes":
        bot.send_message(person, 'Какой у тебя средний балл аттестата?')
        bot.register_next_step_handler(call.message, score_question)
    elif call.data == 'no':
        price = True
        cont(call.message)    
        
@bot.message_handler(content_types=['text'])
def start(message):
    global person
    person = message.from_user.id
    question = "Привет! Куда ты планируешь поступить?"
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Колледж', callback_data='collage'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='ВУЗ', callback_data='VUZ');
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

def score_question(message):
    global score
    score = float(message.text)
    price = False
    cont(message)
    
def collage(message):
    global score
    question = "Хочешь выбрать бюджетное место?"
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no)
    bot.send_message(person, text=question, reply_markup=keyboard)

def cont(message):
    global score
    global person
    bot.send_message(person, 'Колледж | Специализация | Кол-во бюджетных мест | Проходной балл | Цена')
    for line in lines:
        if line == '':
            continue
        curr_score = float(line.split('|')[3])
        if score >= curr_score and curr_score != 0:
            bot.send_message(person, line)
    

if __name__ == '__main__':
     bot.infinity_polling()
