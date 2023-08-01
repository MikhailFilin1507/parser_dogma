import telebot
from telebot import types
from datetime import date
import time
import openpyxl

projects = {
    'ПИК' : [],
    'Самолет' : []
}


bot = telebot.TeleBot('')




@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'pik':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Измайловский лес', callback_data='izm_les'))
        markup.add(types.InlineKeyboardButton('Жулебино', callback_data='pik_zhulebino'))
        markup.add(types.InlineKeyboardButton('Яуза парк', callback_data='pik_yauza'))
        markup.add(types.InlineKeyboardButton('Белая Дача парк', callback_data='pik_bd_park'))
        bot.send_message(callback.message.chat.id, 'Выберите проект', reply_markup=markup)
    elif callback.data == 'samolet':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Люберцы', callback_data='smlt_lyubercy'))
        markup.add(types.InlineKeyboardButton('Долина Яузы', callback_data='smlt_d_yauzy'))
        bot.send_message(callback.message.chat.id, 'Выберите проект', reply_markup=markup)


    elif callback.data == 'izm_les':
        bot.send_message(callback.message.chat.id, 'Считаю, подождите, пожалуйста')
        import izm_les
        bot.send_message(callback.message.chat.id, str(izm_les.parse()))
        time.sleep(3)
        with open(f'data/{str(date.today())}_pik_izm_les.xlsx', 'rb') as f:
            bot.send_document(callback.message.chat.id, f)

    elif callback.data == 'pik_zhulebino':
        bot.send_message(callback.message.chat.id, 'Считаю, подождите, пожалуйста')
        import zhulebino
        bot.send_message(callback.message.chat.id, str(zhulebino.parse()))
        time.sleep(3)
        with open(f'data/{str(date.today())}_pik_zhulebino.xlsx', 'rb') as f:
            bot.send_document(callback.message.chat.id, f)

    elif callback.data == 'pik_yauza':
        bot.send_message(callback.message.chat.id, 'Считаю, подождите, пожалуйста')
        import yauza
        bot.send_message(callback.message.chat.id, str(yauza.parse()))
        time.sleep(3)
        with open(f'data/{str(date.today())}_pik_yauza.xlsx', 'rb') as f:
            bot.send_document(callback.message.chat.id, f)

    elif callback.data == 'pik_bd_park':
        bot.send_message(callback.message.chat.id, 'Считаю, подождите, пожалуйста')
        import bd_park
        bot.send_message(callback.message.chat.id, str(bd_park.parse()))
        time.sleep(3)
        with open(f'data/{str(date.today())}_pik_bd_park.xlsx', 'rb') as f:
            bot.send_document(callback.message.chat.id, f)

    elif callback.data == 'smlt_lyubercy':
        bot.send_message(callback.message.chat.id, 'Считаю, подождите, пожалуйста')
        import samolet_lyubercy
        bot.send_message(callback.message.chat.id, str(samolet_lyubercy.parse()))
        time.sleep(3)
        with open(f'data/{str(date.today())}_smlt_lyubercy.xlsx', 'rb') as f:
            bot.send_document(callback.message.chat.id, f)

    elif callback.data == 'smlt_d_yauzy':
        bot.send_message(callback.message.chat.id, 'Считаю, подождите, пожалуйста')
        import smlt_d_yauzy
        bot.send_message(callback.message.chat.id, str(smlt_d_yauzy.parse()))
        time.sleep(3)
        with open(f'data/{str(date.today())}_smlt_d_yauzy.xlsx', 'rb') as f:
            bot.send_document(callback.message.chat.id, f)

@bot.message_handler()
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('ПИК', callback_data='pik'))
    markup.add(types.InlineKeyboardButton('Самолет', callback_data='samolet'))
    bot.send_message(message.chat.id, 'Выберите застройщика', reply_markup=markup)



bot.polling(none_stop=True) #команда будет постоянно выполняться

