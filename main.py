import telebot
from telebot import types
from configuration.config import *

statuss = ['creator', 'administrator', 'member']
bot = telebot.TeleBot('6844167678:AAEE4fgplauoAMuw0M1mWrwH1MyvG8m3wpM')

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    print(user_id)
    print(type(user_id))
    if user_id in admins:
        markup = types.InlineKeyboardMarkup()
        itembtn = types.InlineKeyboardButton('Изменить', callback_data='Изменить')
        markup.add(itembtn)
        bot.send_message(user_id, "Вы администратор. Вы можете изменять обязательные для подписки каналы.", reply_markup=markup)
    
    else:
        markup = types.InlineKeyboardMarkup()
        itembtn = types.InlineKeyboardButton('Добавиться', callback_data='Добавиться')
        markup.add(itembtn)
        bot.send_message(message.chat.id,"Привет, Я могу помочь тебе добавиться в нашу группу. Для этого нажми кнопку", reply_markup=markup)

    

@bot.message_handler(content_types=['text'])
def get_text_messages(message):    
    first_word = message.text.split()[0] 
    if first_word == "удалить":
        channel = ' '.join(message.text.split()[1:])
        if channel in have_to_sub:
            have_to_sub.remove(channel)
            bot.send_message(message.chat.id, f'Канал {channel} удален')
        else:
            bot.send_message(message.chat.id, f'Канала {channel} нет в обязательном списке для подписки')
    elif first_word == "добавить":
        channel = ' '.join(message.text.split()[1:])
        if channel in have_to_sub:
            bot.send_message(message.chat.id, f'Канал {channel} уже добавлен')
        else:
            have_to_sub.append(channel)
            bot.send_message(message.chat.id, f'Канал {channel} добавлен')

    else:
        user_id = message.from_user.id
        if user_id in admins:
            markup = types.InlineKeyboardMarkup()
            itembtn = types.InlineKeyboardButton('Изменить', callback_data='Изменить')
            markup.add(itembtn)
            bot.send_message(user_id, "Вы администратор. Вы можете изменять обязательные для подписки каналы.", reply_markup=markup)
        
        else:
            markup = types.InlineKeyboardMarkup()
            itembtn = types.InlineKeyboardButton('Добавиться', callback_data='Добавиться')
            markup.add(itembtn)
            bot.send_message(message.chat.id,"Привет, Я могу помочь тебе добавиться в нашу группу. Для этого нажми кнопку", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def button1(callback):
    if callback.data == 'Изменить':
        markup = types.InlineKeyboardMarkup()
        itembtn = types.InlineKeyboardButton('Добавить', callback_data='Добавить')
        itembtn2 = types.InlineKeyboardButton('Удалить', callback_data='Удалить')    
        markup.add(itembtn, itembtn2)
        bot.send_message(callback.message.chat.id, f'Для добавления/удаления обязательного канала, нажмите одну из кнопок снизу', reply_markup=markup)
        
    elif callback.data == 'Удалить':
        k = "\n"
        bot.send_message(callback.message.chat.id, f'Скопируйте и вставьте одно из названий каналов ниже. Также не забудьте вставить "удалить" перед названием канала. \n"\n{k.join(have_to_sub)}')

    elif callback.data == 'Добавить':
        bot.send_message(callback.message.chat.id, f'Напишите username канала. Также не забудьте вставить "добавить " перед названием канала.')

    elif callback.data == 'Добавиться':
        left_or_not = []
        count = 0
        for i in range(len(have_to_sub)):
            res = bot.get_chat_member(chat_id=have_to_sub[i], user_id=callback.message.chat.id)
            print(have_to_sub[i])
            left_or_not.append(res.status)
            if res.status not in statuss:
                count += 1
        if count != 0:
            urlt = 't.me/'
            mark = types.InlineKeyboardMarkup()
            kons = []
            for i in range(len(left_or_not)):
                if left_or_not[i] not in statuss:
                    kons.append(types.InlineKeyboardButton(have_to_sub[i], url=urlt + have_to_sub[i][1:]))
            kons.append(types.InlineKeyboardButton('Подписался✅', callback_data='check'))
            for i in kons:
                mark.add(i)
            bot.send_message(callback.message.chat.id, f'Вам необходимо подписаться на следующие каналы:', reply_markup=mark)
        else:
            #мне нужно добавлять пользователя в группу, через его user_id
            bot.send_message(callback.message.chat.id, f'Присоединяйтесь к каналу!\n {group}')

    elif callback.data == 'check':
        left_or_not = []
        count = 0
        for i in range(len(have_to_sub)):
            res = bot.get_chat_member(chat_id=have_to_sub[i], user_id=callback.message.chat.id)
            left_or_not.append(res.status)
            if res.status not in statuss:
                count += 1
        if count != 0:
            urlt = 't.me/'
            mark = types.InlineKeyboardMarkup()
            kons = []
            for i in range(len(left_or_not)):
                if left_or_not[i] not in statuss:
                    kons.append(types.InlineKeyboardButton(have_to_sub[i], url=urlt + have_to_sub[i][1:]))
            kons.append(types.InlineKeyboardButton('Подписался✅', callback_data='check'))
            for i in kons:
                mark.add(i)
            bot.send_message(callback.message.chat.id, f'Вам все еще необходимо подписаться на следующие каналы:', reply_markup=mark)

        else:
            bot.send_message(callback.message.chat.id, f'Присоединяйтесь к каналу!\n {group}')



bot.infinity_polling(none_stop=True)
