import telebot
from telebot import types
import random


words_dict = {}
with open("words_coper.txt", "r", encoding='utf-8') as file:
    words_list = file.read().split('\n')[:-1]
    for i in words_list:
        word = i.split('$')
        words_dict[word[0]] = word[1] # words_dict = {'слово на русском': 'word on english'}

# print(words_dict)

bot = telebot.TeleBot('API-KEY')

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('Пишем')
    keyboard.add(button1)
    bot.reply_to(message, 'Бот работает так: он пишет слово на русском, а вы должны писать его на английском', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_message(message):

    def shuffle_dict(input_dict):
        items = list(input_dict.items())
        random.shuffle(items)
        return dict(items)

    words_dict2 = shuffle_dict(words_dict)
    print(words_dict2)
    chat_id = message.chat.id
    if message.text == 'Пишем':
        words = iter(words_dict2.items())
        def write():
            try:
                word, rigth_answer = next(words)
                msg = bot.send_message(chat_id, word)
                print(message.text)

                def examination(message):
                    if (message.text).lower() == rigth_answer:
                        bot.send_message(chat_id, f'🟢{rigth_answer}🟢')
                        write()
                    else:
                        bot.send_message(chat_id, f'🔴{rigth_answer}🔴')
                        write()

                bot.register_next_step_handler(msg, examination)

            except StopIteration:
                bot.send_message(chat_id, 'Слова закончились')
        write()

bot.polling(none_stop=True)
