import telebot
from telebot import types

token = '1474894095:AAFzxnYb1RMQLx_ehCkYqSpZO0uFo2a9Es4'
bot = telebot.TeleBot(token)

class Hash_location():
    location_id = dict()
    message_chat_id = int()

    def add_location(self, message_chat_id, message_location_latitude, message_location_longitude):
        try:
            list_loc = list(self.location_id[message_chat_id])
        except:
            list_loc = list()
        list_loc.append((message_location_latitude, message_location_longitude))
        self.location_id[message_chat_id] = list_loc

    def list_location(self, message_chat_id):
        try:
            if self.location_id[message_chat_id] == []:
                return "Я забыл где Вы были, добавьте место и я попытаюсь его запомнить."
            bot.send_message(message_chat_id, "Вот список мест на моей памяти:")
            return str(self.location_id[message_chat_id])
        except KeyError:
            return "Впервые вижу Вас, давайте запомним это место встречи"

    def reset_location(self, message_chat_id):
        try:
            if self.location_id[message_chat_id]:
                self.location_id[message_chat_id] = list()
                return "Готово! Я отправил список мест в BlackHole"
            return "Не переживайте, Я точно все удалил)"
        except KeyError:
            bot.send_sticker(message_chat_id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
            return "Вы обнулили меня раньше времени ^_^, готов служить Вам еще дольше)"


@bot.message_handler(commands=["start"])
def geo(message):
    bot.send_message(message.chat.id, 'Привет, попробуй такие команды как: \n/add: добавить место \n/list: список мест  \n/reset: очистить список')


@bot.message_handler(commands=["add"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Нажмите на кнопку чтобы сохранить это место.", reply_markup=keyboard)

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        a = Hash_location()
        a.message_chat_id = message.chat.id
        a.add_location(message.chat.id, message.location.latitude, message.location.longitude)


@bot.message_handler(commands=["list"])
def list_geo(message):
    a = Hash_location().list_location(message.chat.id)
    bot.send_message(message.chat.id, a)


@bot.message_handler(commands=["reset"])
def reset(message):
    a = Hash_location().reset_location(message.chat.id)
    bot.send_message(message.chat.id, a)


bot.polling()
