import config
import telebot
import server_side as server
from telebot import types

bot = telebot.TeleBot(config.teletoken)

@bot.message_handler(commands = ['start'])
def say_hi(message):
    startmenu = types.ReplyKeyboardMarkup(True, True)
    startmenu.row(config.default_city1, config.default_city2, config.default_city3)
    startmenu.row('Выбрать другой город')
    send = bot.send_message(message.chat.id, 'Данный бот позволяет узнать текущую погоду или прогноз погоды для вашего города.'
    + '\n\nВыберите город из списка ниже, либо введите название своего города', reply_markup=startmenu)
    bot.register_next_step_handler(send, choose_mode)


@bot.message_handler(content_types = ['text'])
def choose_mode(message):
    if message.text == 'Выбрать другой город':
        send = bot.send_message(message.chat.id, 'Напишите название интересующего вас города')
        bot.register_next_step_handler(send, choose_mode)
    elif message.text == 'Отмена':
        say_clone(message)
    elif message.text == config.to_start_key:
        say_clone(message)
    else:
        # config.chosen_city.insert(0 ,message.text) - строчка для хранения города в массиве
        config.selected_city[message.chat.id] = message.text
        mode_menu = types.ReplyKeyboardMarkup(True, False)
        mode_menu.row('Погода сейчас', 'Погода на завтра', 'Погода на период')
        mode_menu.row('Отмена')
        send = bot.send_message(message.chat.id, 'Выберите что именно вас интересует:', reply_markup=mode_menu)
        bot.register_next_step_handler(send, result)

def result(message):
    if message.text == 'Отмена':
        say_clone(message)
    elif message.text == 'Погода сейчас':
        to_start = types.ReplyKeyboardMarkup(True, True)
        to_start.row(config.to_start_key)
        bot.send_message(message.chat.id, server.today_weather(config.selected_city[message.chat.id]), reply_markup=to_start)
        config.selected_city.pop(message.chat.id)
    elif message.text == 'Погода на завтра':
        to_start = types.ReplyKeyboardMarkup(True, True)
        to_start.row(config.to_start_key)
        bot.send_message(message.chat.id, server.tomorrow_weather(config.selected_city[message.chat.id]), reply_markup=to_start)
        config.selected_city.pop(message.chat.id)
    else:
        # Вместо этого нужно расписать варианты работы с каждым режимом прогноза
        bot.send_message(message.chat.id, 'Ваш город: ' + config.selected_city[message.chat.id])
        print(config.selected_city)
        config.selected_city.pop(message.chat.id)


def say_clone(message):
    startmenu = types.ReplyKeyboardMarkup(True, True)
    startmenu.row(config.default_city1, config.default_city2, config.default_city3)
    startmenu.row('Выбрать другой город')
    send = bot.send_message(message.chat.id, 'Данный бот позволяет узнать текущую погоду или прогноз погоды для вашего города.'
    + '\n\nВыберите город из списка ниже, либо введите название своего города', reply_markup=startmenu)
    bot.register_next_step_handler(send, choose_mode)

        



bot.polling()
# if __name__ == '__main__':
#     while True:
#         try:
#             bot.polling(none_stop=True)
#         except Exception as e:
#             time.sleep(3)
#             print(e)   