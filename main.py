import telebot
from telebot import types
import random

def creat_words():
    words_dict = {}
    with open("words_coper.txt", "r", encoding='utf-8') as file:
        words_list = file.read().split('\n')[:-1]
        for i in words_list:
            word = i.split('$')
            words_dict[word[0]] = word[1] # words_dict = {'слово на русском': 'word on english'}

    def shuffle_dict(input_dict):
        items = list(input_dict.items())
        random.shuffle(items)
        return dict(items)
    words_dict2 = shuffle_dict(words_dict)

    return words_dict2

users = {}
blacklisted_users = [1424647121, 1047167628, 1826740802, 2019061170]
active_tests = set()


bot = telebot.TeleBot('7998808652:AAEXyWyGuo3gjfZyryQOIlm6FU73s0JgFn0')

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    if chat_id in blacklisted_users:
        return

    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('Начать тест')
    keyboard.add(button1)
    bot.reply_to(message, 'Бот работает так: он пишет слово на русском, а вы должны писать его на английском. Чтобы начать нажмите на кнопку "Начать тест"', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Начать тест")
def handle_message(message):
    chat_id = message.chat.id

    if chat_id in blacklisted_users:
        return

    if chat_id in active_tests:
        return

    active_tests.add(chat_id)
    print(active_tests)
    remove_keyboard = types.ReplyKeyboardRemove()
    words_dict = creat_words()
    wrong_words = {}
    users[chat_id] = [words_dict, wrong_words]


    def write(func_chat_id):
        if users[func_chat_id][0] != {}:
            def examination(message):
                if message.text.lower() == '/stop':
                    keyboard = types.ReplyKeyboardMarkup()
                    button1 = types.KeyboardButton('Начать тест')
                    keyboard.add(button1)
                    bot.send_message(chat_id, 'Тест остановлен', reply_markup=keyboard)
                    active_tests.discard(func_chat_id)
                    return creat_words

                if message.text.lower() == rigth_answer:
                    bot.send_message(chat_id, f'🟢{rigth_answer}🟢')
                    try:
                        del users[func_chat_id][0][word]
                        del users[func_chat_id][1][word]
                    except: None
                    print(f'{message.from_user.first_name} Слов осталось : {len(users[func_chat_id][0])}, неправильных слов: {len(users[func_chat_id][1])}, {func_chat_id}')
                    write(chat_id)
                else:
                    bot.send_message(chat_id, f'🔴{rigth_answer}🔴')
                    try:
                        del users[func_chat_id][0][word]
                    except: None
                    users[func_chat_id][1][word] = rigth_answer
                    print(f'{message.from_user.first_name} Слов осталось : {len(users[func_chat_id][0])}, неправильных слов: {len(users[func_chat_id][1])}, {func_chat_id}')
                    write(chat_id)

            word = next(iter(users[func_chat_id][0]))
            rigth_answer = users[func_chat_id][0][word]
            msg = bot.send_message(chat_id, word, reply_markup=remove_keyboard)
            bot.register_next_step_handler(msg, examination)

        if users[func_chat_id][0] == {} and users[func_chat_id][1] == {}:
            keyboard = types.ReplyKeyboardMarkup()
            button1 = types.KeyboardButton('Начать тест')
            keyboard.add(button1)
            active_tests.discard(func_chat_id)
            bot.send_message(chat_id, 'Все слова верные, хорошая работа!', reply_markup=keyboard)

        if users[func_chat_id][0] == {} and users[func_chat_id][1] != {}:
            bot.send_message(chat_id, 'Работа над ошибками')
            users[func_chat_id][0], users[func_chat_id][1] = users[func_chat_id][1], users[func_chat_id][0]
            write(chat_id)

    print(message.from_user.first_name, message.from_user.last_name, message.from_user.username, chat_id)
    write(chat_id)



bot.polling(none_stop=True)