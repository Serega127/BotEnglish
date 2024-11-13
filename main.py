import telebot
from telebot import types
import random
import os
import sys
import time


def craet_words():
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

words_dict = {}
with open("words_coper.txt", "r", encoding='utf-8') as file:
    words_list = file.read().split('\n')[:-1]
    for i in words_list:
        word = i.split('$')
        words_dict[word[0]] = word[1] # words_dict = {'слово на русском': 'word on english'}

print(words_dict)

bot = telebot.TeleBot('7998808652:AAEXyWyGuo3gjfZyryQOIlm6FU73s0JgFn0')

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('Пишем')
    keyboard.add(button1)
    bot.reply_to(message, 'Бот работает так: он пишет слово на русском, а вы должны писать его на английском. Чтобы начать нажмите на кнопку "Пишем"', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Пишем")
def handle_message(message):

    def shuffle_dict(input_dict):
        items = list(input_dict.items())
        random.shuffle(items)
        return dict(items)
    words_dict2 = shuffle_dict(words_dict)
    wrong_words = {}

    chat_id = message.chat.id

    def write(dct):
        if dct != {}:
            def examination(message):
                if message.text.lower() == '/stop':
                    bot.send_message(chat_id, 'Тест остановлен')
                    return craet_words

                if message.text.lower() == rigth_answer:
                    bot.send_message(chat_id, f'🟢{rigth_answer}🟢')
                    del dct[word]

                    try:
                        del wrong_words[word]
                    except: None
                    write(dct)
                else:
                    bot.send_message(chat_id, f'🔴{rigth_answer}🔴')
                    del dct[word]
                    wrong_words[word] = rigth_answer
                    write(dct)

            word = next(iter(dct))
            rigth_answer = dct[word]
            msg = bot.send_message(chat_id, word)
            bot.register_next_step_handler(msg, examination)

        if dct == {} and wrong_words == {}:
            bot.send_message(chat_id, 'Все слова верные, хорошая работа!')

        if dct == {} and wrong_words != {}:
            bot.send_message(chat_id, 'Работа над ошибками')
            words_dict2 = wrong_words.copy()
            write(words_dict2)

    write(words_dict2)


@bot.message_handler(commands=['restart'])
def restart(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Бот перезапускается...")
    bot.stop_polling()  # Завершаем текущий процесс polling
    time.sleep(1)  # Небольшая пауза, чтобы завершить процессы
    os.execv(sys.executable, [sys.executable] + sys.argv)  # Перезапускаем бот



bot.polling(none_stop=True)