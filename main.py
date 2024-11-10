import telebot

with open("words_coper.txt", "r", encoding='utf-8') as file:
    words_list = file.read().split('\n')[:-1]
    words_dict = {}
    for i in words_list:
        word = i.split('$')
        words_dict[word[0]] = word[1] # words_dict = {'слово на русском': 'word on english'}

# print(words_dict)

words = iter(words_dict.items())
# def cikcle():
#     try:
#         word = next(words)
#         print(word)
#         word = next(words)
#         print(word)
#         word = next(words)
#         print(word)
#         word = next(words)
#         print(word)
#         word = next(words)
#         print(word)
#     except StopIteration:
#         print('Конец')
#
# cikcle()

bot = telebot.TeleBot('API_KEY')

@bot.message_handler(commands=['help'])
def start_handler(message):
    bot.reply_to(message, 'Список доступных команд:\ /start — начать работу с ботом\ /help — получить справку о работе бота.')


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_support = telebot.types.KeyboardButton(text="Пишем")
    keyboard.add(button_support)

# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):






bot.polling(none_stop=True)