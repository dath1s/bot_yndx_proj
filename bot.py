import sqlite3
import telebot
import emoji
from funcs import *
from data import db_session
from data.users import User
from menu import *
from telebot.types import LabeledPrice, ShippingOption
from telebot import types
import random

db_session.global_init("db/users.db")

bot = telebot.TeleBot('1111111111:AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQR')

provider_token = '111111111:TEST:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'

non_understands = [emoji.emojize('Извини, но моя твоя не понимать :zipper-mouth_face:'),
                   emoji.emojize('Дружище, не понял тебя :thinking_face:'),
                   emoji.emojize('Не совсем понял тебя, брат :face_without_mouth:')]

cur = sqlite3.connect('db/users.db', check_same_thread=False)


markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

button1 = types.KeyboardButton(text=emoji.emojize('Меню :notebook_with_decorative_cover:'))
button2 = types.KeyboardButton(text=emoji.emojize('Корзина :takeout_box:'))
button3 = types.KeyboardButton(text=emoji.emojize('Тех. поддержка :SOS_button:'))

markup.add(*[button1, button2])
markup.add(button3)


markup_order = reply_markup_maker(3,
                                  ['Очистить корзину', 'Заказать', 'Назад'],
                                  True)

markup_food_type = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
button1 = types.KeyboardButton(text=emoji.emojize('Закуски :sandwich:'))
button2 = types.KeyboardButton(text=emoji.emojize('Салаты :green_salad:'))
button3 = types.KeyboardButton(text=emoji.emojize('Горячие блюда :meat_on_bone:'))
button4 = types.KeyboardButton(text=emoji.emojize('Супы :bowl_with_spoon:'))
button5 = types.KeyboardButton(text=emoji.emojize('Гарниры :french_fries:'))
button6 = types.KeyboardButton(text=emoji.emojize('Блюда на огне :shallow_pan_of_food:'))
button7 = types.KeyboardButton(text=emoji.emojize('Соусы :hot_pepper:'))
button8 = types.KeyboardButton(text=emoji.emojize('Десерты :shortcake:'))
button9 = types.KeyboardButton(text=emoji.emojize('Напитки :cocktail_glass:'))
button10 = types.KeyboardButton(text='Назад')

markup_food_type.add(*[button1, button2, button3])
markup_food_type.add(*[button4, button5, button6])
markup_food_type.add(*[button7, button8, button9])
markup_food_type.add(button10)


markup_snacks = inline_markup_maker(8,
                                    [i for i in snacks_name_tag.keys()],
                                    [snacks_name_tag[i].replace('/', '') for i in snacks_name_tag.keys()],
                                    1)

markup_salads = inline_markup_maker(8,
                                    [i for i in salad_name_tag.keys()],
                                    [salad_name_tag[i].replace('/', '') for i in salad_name_tag.keys()],
                                    1)

markup_hot_food = inline_markup_maker(8,
                                      [i for i in hot_food_name_tag.keys()],
                                      [hot_food_name_tag[i].replace('/', '') for i in hot_food_name_tag.keys()],
                                      1)

markup_soup = inline_markup_maker(5,
                                  [i for i in soup_name_tag.keys()],
                                  [soup_name_tag[i].replace('/', '') for i in soup_name_tag.keys()],
                                  1)

markup_side_dish = inline_markup_maker(3,
                                       [i for i in side_dishes_name_tag.keys()],
                                       [side_dishes_name_tag[i].replace('/', '') for i in side_dishes_name_tag.keys()],
                                       1)

markup_on_fire = inline_markup_maker(8,
                                     [i for i in on_fire_name_tag.keys()],
                                     [on_fire_name_tag[i].replace('/', '') for i in on_fire_name_tag.keys()],
                                     1)

markup_sous = inline_markup_maker(4,
                                  [i for i in sous_name_tag.keys()],
                                  [sous_name_tag[i].replace('/', '') for i in sous_name_tag.keys()],
                                  1)

markup_deserts = inline_markup_maker(8,
                                     [i for i in deserts_name_tag.keys()],
                                     [deserts_name_tag[i].replace('/', '') for i in deserts_name_tag.keys()],
                                     1)

markup_drinks = inline_markup_maker(7,
                                    [i for i in drink_name_tag.keys()],
                                    [drink_name_tag[i].replace('/', '') for i in drink_name_tag.keys()],
                                    1)


markup_how_r_u = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button1 = types.KeyboardButton(text=emoji.emojize('Супер! :grinning_face:'))
button2 = types.KeyboardButton(text=emoji.emojize('Ну, такое... :pensive_face:'))
button3 = types.KeyboardButton(text='Назад')

markup_how_r_u.add(*[button1, button2])
markup_how_r_u.add(button3)

@bot.message_handler(commands=['start'])
def welcome(message):
    is_in_db = list(
        cur.execute(f"""SELECT user_name FROM users WHERE user_telegram_id = {message.from_user.id}"""))

    if is_in_db:
        bot.send_message(message.from_user.id, emoji.emojize(
            f'Какие люди, мать моя женщина!:grinning_face_with_smiling_eyes:\n'
            f'Давно не виделись, {is_in_db[0][0]}. Проходи, не стесняйся.'
            '\nЯ, Вах Ашот, подберу тебя блюда на самые разные случаи жизни,'
            'начиная от люля-кебаб и заканчивая шашлыком во фритюре. Всё, что твоя душа пожелает!'
        ))
        bot.send_message(message.from_user.id,
                         'Чего на этот раз пожелаешь?',
                         reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, emoji.emojize(
            f'Здраствуй, мой дрогой!:grinning_face_with_smiling_eyes:\n'
            f'Добро пожаловать в моё онлайн кафе VahAshot\n'
            '\nЯ, Вах Ашот, подберу тебя блюда на самые разные случаи жизни,'
            'начиная от люля-кебаб и заканчивая шашлыком во фритюре. Всё, что твоя душа пожелает!\n\n'
            'Но для для начала, скажи, как тебя зовут, дорогой мой посетитель. Пожалуйста, напиши сообщение:'
            '"Моё имя ..."'
        ))


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.chat.type == 'private':
        db_sess = db_session.create_session()
        price = 0

        is_in_db = list(
            cur.execute(f"""SELECT user_name FROM users WHERE user_telegram_id = {message.from_user.id}"""))
        try:
            if not is_in_db:
                if 'моё имя ' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Какое прекрасное у тебя имя!'))
                    bot.send_message(message.from_user.id,
                                     'Итак, с чего начнем?',
                                     reply_markup=markup)

                    user = User()

                    user.user_name = message.text.split()[-1]
                    user.user_telegram_id = message.from_user.id
                    user.bin = '[]'
                    user.price = 0

                    db_sess.add(user)

                    db_sess.commit()

                elif 'нарды' in message.text.lower() and any([i in message.text.lower() for i in
                                                              ['играть', 'сыграем', 'поиграем', 'play', 'поиграть',
                                                               'каточку']]):
                    bot.send_message(message.from_user.id,
                                     'Только после нашего знакомства. '
                                     'Пока я наливаю чай, напиши своё имя! '
                                     '\n(Пожалуйста, напиши сообщение: "Моё имя ...")')

                else:
                    bot.send_message(message.from_user.id, emoji.emojize(
                        f'Для начала, познакомимся!:grinning_face_with_smiling_eyes:\n'
                        f'(Пожалуйста, напиши сообщение: "Моё имя ...")'
                    ))

            else:
                if message.text in [f'/snack{i}' for i in range(1, 9)]:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str(eval(user.bin) + [get_key(snacks_name_tag, message.text)])
                    user.price = user.price + int(
                        snacks_name_price[get_key(snacks_name_tag, message.text)].replace(' руб.', ''))
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     'Блюдо добавлено в корзину')

                elif message.text in [f'/salad{i}' for i in range(1, 9)]:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str(eval(user.bin) + [get_key(salad_name_tag, message.text)])
                    user.price = user.price + int(
                        salad_name_price[get_key(salad_name_tag, message.text)].replace(' руб.', ''))
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     'Блюдо добавлено в корзину')

                elif message.text in [f'/hot_food{i}' for i in range(1, 9)]:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str(eval(user.bin) + [get_key(hot_food_name_tag, message.text)])
                    user.price = user.price + int(
                        hot_food_name_price[get_key(hot_food_name_tag, message.text)].replace(' руб.', ''))
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     'Блюдо добавлено в корзину')

                elif message.text in [f'/soup{i}' for i in range(1, 6)]:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str(eval(user.bin) + [get_key(soup_name_tag, message.text)])
                    user.price = user.price + int(
                        soup_name_price[get_key(soup_name_tag, message.text)].replace(' руб.', ''))
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     'Блюдо добавлено в корзину')

                elif message.text in [f'/side_dish{i}' for i in range(1, 4)]:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str(eval(user.bin) + [get_key(side_dishes_name_tag, message.text)])
                    user.price = user.price + int(
                        side_dishes_name_price[get_key(side_dishes_name_tag, message.text)].replace(' руб.', ''))
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     'Блюдо добавлено в корзину')

                elif message.text in [f'/on_fire{i}' for i in range(1, 9)]:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str(eval(user.bin) + [get_key(on_fire_name_tag, message.text)])
                    user.price = user.price + int(
                        on_fire_name_price[get_key(on_fire_name_tag, message.text)].replace(' руб.', ''))
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     'Блюдо добавлено в корзину')

                elif message.text in [f'/sauces{i}' for i in range(1, 5)]:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str(eval(user.bin) + [get_key(soup_name_tag, message.text)])
                    user.price = user.price + int(
                        soup_name_price[get_key(sous_name_tag, message.text)].replace(' руб.', ''))
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     'Соус добавлен в корзину')

                elif message.text in [f'/deserts{i}' for i in range(1, 9)]:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str(eval(user.bin) + [get_key(deserts_name_tag, message.text)])
                    user.price = user.price + int(
                        deserts_name_price[get_key(deserts_name_tag, message.text)].replace(' руб.', ''))
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     'Блюдо добавлено в корзину')

                elif message.text in [f'/drinks{i}' for i in range(1, 8)]:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str(eval(user.bin) + [get_key(drink_name_tag, message.text)])
                    user.price = user.price + int(
                        drink_name_price[get_key(drink_name_tag, message.text)].replace(' руб.', ''))
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     'Напиток добавлен в корзину')

                elif 'моё имя ' in message.text.lower():
                    bot.send_message(message.from_user.id, emoji.emojize(
                        'Дорогой мой, как я могу тебя забыть!:grinning_face_with_smiling_eyes:'))

                elif 'нарды' in message.text.lower() and any([i in message.text.lower() for i in
                                                              ['играть', 'сыграем', 'поиграем', 'play', 'поиграть',
                                                               'каточку']]):
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Заходи, поиграем :money-mouth_face: \n https://minigames.mail.ru/nardy_dlinnye'))

                elif 'меню' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     'Выберите тип блюда котрое хотите заказать:',
                                     reply_markup=markup_food_type)

                elif emoji.emojize("Оплатить... :money_with_wings:") == message.text:
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    prices = [LabeledPrice(label='Ваш заказ', amount=user.price * 100)]

                    bot.send_invoice(message.chat.id, title='Ваш заказ',
                                     description='Оплатите заказ любым удобным вам способом',
                                     provider_token='381764678:TEST:36042',
                                     currency='RUB',
                                     photo_url='https://blog-food.ru/images/site/recipes/main-dishes/0220-kebab/18.jpg',
                                     photo_height=512,  # !=0/None or picture won't be shown
                                     photo_width=512,
                                     photo_size=512,
                                     is_flexible=False,  # True If you need to set up Shipping Fee
                                     prices=prices,
                                     start_parameter='example',
                                     invoice_payload='COUPON')

                elif 'корзина' in message.text.lower():
                    bin_str = {}
                    bin_list = [eval(str(i).split(':')[-1]) for i in
                                db_sess.query(User).filter(User.user_telegram_id == message.from_user.id)][0]

                    for i in bin_list:
                        bin_str[i] = bin_list.count(i)

                    ans = '\n'.join([f'{i}: <b>{bin_str[i]} шт.</b>' for i in
                                     bin_str.keys()]) if bin_list != [] else emoji.emojize('Твоя корзина пуста, дорогой :frowning_face:')

                    if ans == emoji.emojize('Твоя корзина пуста, дорогой :frowning_face:'):
                        bot.send_message(message.from_user.id,
                                         ans,
                                         parse_mode='html')
                    else:
                        bot.send_message(message.from_user.id,
                                         ans,
                                         parse_mode='html',
                                         reply_markup=markup_order)

                elif any(i in message.text.lower() for i in
                         ['забегаловки', 'кафе', 'рестараны', 'забегаловка', 'ресторан']):
                    pass

                elif 'поддержка' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     '<b>Если нужна помощь Ашота:</b>'
                                     '\n<b>Телефон</b>: +7-999-876-54-32'
                                     '\n<b>Почта</b>: vahashot_help@gmail.com',
                                     parse_mode='html')

                elif 'Назад' == message.text:
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Что я могу сделать для тебя, дорогой друг мой? :upside-down_face:'),
                                     reply_markup=markup)

                elif 'закуски' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Нажми на интересующую тебя закуску и я пришлю тебе все, что знаю про неё :beaming_face_with_smiling_eyes:'),
                                     reply_markup=markup_snacks)

                elif 'салаты' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Нажми на интересующий тебя салат и я пришлю тебе все, что знаю про него :beaming_face_with_smiling_eyes:'),
                                     reply_markup=markup_salads)

                elif 'горячие блюда' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Нажми на интересующее тебя блюдо и я пришлю тебе все, что знаю про него :beaming_face_with_smiling_eyes:'),
                                     reply_markup=markup_hot_food)

                elif 'супы' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Нажми на интересующий тебя суп и я пришлю тебе все, что знаю про него :beaming_face_with_smiling_eyes:'),
                                     reply_markup=markup_soup)

                elif 'гарниры' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Нажми на интересующее тебя блюдо и я пришлю тебе все, что знаю про него :beaming_face_with_smiling_eyes:'),
                                     reply_markup=markup_side_dish)

                elif 'блюда на огне' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Нажми на интересующее тебя блюдо и я пришлю тебе все, что знаю про него :beaming_face_with_smiling_eyes:'),
                                     reply_markup=markup_on_fire)

                elif 'соусы' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Нажми на интересующий тебя соус и я пришлю тебе все, что знаю про него :beaming_face_with_smiling_eyes:'),
                                     reply_markup=markup_sous)

                elif 'десерты' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Нажми на интересующий тебя десерт и я пришлю тебе все, что знаю про него :beaming_face_with_smiling_eyes:'),
                                     reply_markup=markup_deserts)

                elif 'напитки' in message.text.lower():
                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Нажми на интересующий тебя напиток и я пришлю тебе все, что знаю про него :beaming_face_with_smiling_eyes:'),
                                     reply_markup=markup_drinks)

                elif 'очистить корзину' in message.text.lower():
                    user = db_sess.query(User).filter(User.user_telegram_id == message.from_user.id).first()

                    user.bin = str([])
                    user.price = 0
                    db_sess.commit()

                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Корзина успешно очищена, дорогой :winking_face:'),
                                     reply_markup=markup)

                elif 'Заказать' == message.text:
                    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

                    button_geo = types.KeyboardButton(text=emoji.emojize("Отправить местоположение :house_with_garden:"), request_location=True)

                    keyboard.add(button_geo)

                    bot.send_message(message.chat.id,
                                     emoji.emojize(
                                         "Поделись местоположением, чтобы я знал, куда доставлять "
                                         ":grinning_face_with_big_eyes:"),
                                     reply_markup=keyboard)

                elif ('как' in message.text.lower() and ('сам' in message.text.lower()
                                                         or 'дела' in message.text.lower()
                                                         or 'живешь' in message.text.lower()
                                                         or 'поживаешь' in message.text.lower()
                                                         or 'ты' in message.text.lower()
                                                         or 'жизнь' in message.text.lower()))\
                        or 'что нов' in message.text.lower():

                    bot.send_message(message.from_user.id,
                                     emoji.emojize('Со мной все в порядке, дорогой :grinning_face_with_smiling_eyes:'
                                                   '\nКак сам-то живешь?'),
                                     reply_markup=markup_how_r_u)

                elif 'супер' in message.text.lower()\
                        or 'норм' in message.text.lower()\
                        or 'хорош' in message.text.lower()\
                        or 'потряс' in message.text.lower()\
                        or 'замечат' in message.text.lower()\
                        or 'прекрас' in message.text.lower():

                    bot.send_message(message.from_user.id,
                                     'Рад за тебя! Может, хочешь заказать поесть?',
                                     reply_markup=markup)

                elif 'такое' in message.text.lower()\
                        or 'плох' in message.text.lower()\
                        or 'не оч' in message.text.lower()\
                        or 'ужас' in message.text.lower()\
                        or 'стрем' in message.text.lower()\
                        or 'печаль' in message.text.lower()\
                        or 'груст' in message.text.lower():

                    bot.send_message(message.from_user.id,
                                     'Очень жаль... Знаешь, я думаю еда от Вах Ашота способна поднять твое настроение!',
                                     reply_markup=markup)

                else:
                    bot.send_message(message.from_user.id,
                                     random.choice(non_understands))

        except Exception:
            bot.send_message(message.from_user.id,
                             random.choice(non_understands))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if 'snack' in call.data:
        number = int(str(call.data)[-1])

        snack_name = list(snacks_name_tag.keys())[number - 1]
        snack_description = snacks_name_description[snack_name]
        snack_price = snacks_name_price[snack_name]
        snack_tag = snacks_name_tag[snack_name]

        bot.send_message(call.message.chat.id,
                         emoji.emojize(f"<b>{snack_name}</b>"
                         f"\n\n<b>Описание</b>:\n{snack_description}\n\n"
                         f"<b>Цена</b>: {snack_price}\n\n"
                         f"Для добавления в корзину нажмите на тэг справа :backhand_index_pointing_right: {snack_tag}"),
                         parse_mode="html")

    elif 'salad' in call.data:
        number = int(str(call.data)[-1])

        salad_name = list(salad_name_tag.keys())[number - 1]
        salad_description = salad_name_description[salad_name]
        salad_price = salad_name_price[salad_name]
        salad_tag = salad_name_tag[salad_name]

        bot.send_message(call.message.chat.id,
                         emoji.emojize(f"<b>{salad_name}</b>"
                         f"\n\n<b>Описание</b>:\n{salad_description}\n\n"
                         f"<b>Цена</b>: {salad_price}\n\n"
                         f"Для добавления в корзину нажмите на тэг справа :backhand_index_pointing_right: {salad_tag}"),
                         parse_mode="html")

    elif 'hot_food' in call.data:
        number = int(str(call.data)[-1])

        hotf_name = list(hot_food_name_tag.keys())[number - 1]
        hotf_description = hot_food_name_description[hotf_name]
        hotf_price = hot_food_name_price[hotf_name]
        hotf_tag = hot_food_name_tag[hotf_name]

        bot.send_message(call.message.chat.id,
                         emoji.emojize(f"<b>{hotf_name}</b>"
                         f"\n\n<b>Описание</b>:\n{hotf_description}\n\n"
                         f"<b>Цена</b>: {hotf_price}\n\n"
                         f"Для добавления в корзину нажмите на тэг справа :backhand_index_pointing_right: {hotf_tag}"),
                         parse_mode="html")

    elif 'soup' in call.data:
        number = int(str(call.data)[-1])

        soup_name = list(soup_name_tag.keys())[number - 1]
        soup_description = soup_name_description[soup_name]
        soup_price = soup_name_price[soup_name]
        soup_tag = soup_name_tag[soup_name]

        bot.send_message(call.message.chat.id,
                         emoji.emojize(f"<b>{soup_name}</b>"
                         f"\n\n<b>Описание</b>:\n{soup_description}\n\n"
                         f"<b>Цена</b>: {soup_price}\n\n"
                         f"Для добавления в корзину нажмите на тэг справа :backhand_index_pointing_right: {soup_tag}"),
                         parse_mode="html")

    elif 'side_dish' in call.data:
        number = int(str(call.data)[-1])

        side_name = list(side_dishes_name_tag.keys())[number - 1]
        side_description = side_dishes_name_description[side_name]
        side_price = side_dishes_name_price[side_name]
        side_tag = side_dishes_name_tag[side_name]

        bot.send_message(call.message.chat.id,
                         emoji.emojize(f"<b>{side_name}</b>"
                         f"\n\n<b>Описание</b>:\n{side_description}\n\n"
                         f"<b>Цена</b>: {side_price}\n\n"
                         f"Для добавления в корзину нажмите на тэг справа :backhand_index_pointing_right: {side_tag}"),
                         parse_mode="html")

    elif 'on_fire' in call.data:
        number = int(str(call.data)[-1])

        fire_name = list(on_fire_name_tag.keys())[number - 1]
        fire_description = on_fire_name_description[fire_name]
        fire_price = on_fire_name_price[fire_name]
        fire_tag = on_fire_name_tag[fire_name]

        bot.send_message(call.message.chat.id,
                         emoji.emojize(f"<b>{fire_name}</b>"
                         f"\n\n<b>Описание</b>:\n{fire_description}\n\n"
                         f"<b>Цена</b>: {fire_price}\n\n"
                         f"Для добавления в корзину нажмите на тэг справа :backhand_index_pointing_right: {fire_tag}"),
                         parse_mode="html")

    elif 'sauces' in call.data:
        number = int(str(call.data)[-1])

        sous_name = list(sous_name_tag.keys())[number - 1]
        sous_description = sous_name_description[sous_name]
        sous_price = sous_name_price[sous_name]
        sous_tag = sous_name_tag[sous_name]

        bot.send_message(call.message.chat.id,
                         emoji.emojize(f"<b>{sous_name}</b>"
                         f"\n\n<b>Описание</b>:\n{sous_description}\n\n"
                         f"<b>Цена</b>: {sous_price}\n\n"
                         f"Для добавления в корзину нажмите на тэг справа :backhand_index_pointing_right: {sous_tag}"),
                         parse_mode="html")

    elif 'deserts' in call.data:
        number = int(str(call.data)[-1])

        desert_name = list(deserts_name_tag.keys())[number - 1]
        desert_description = deserts_name_description[desert_name]
        desert_price = deserts_name_price[desert_name]
        desert_tag = deserts_name_tag[desert_name]

        bot.send_message(call.message.chat.id,
                         emoji.emojize(f"<b>{desert_name}</b>"
                         f"\n\n<b>Описание</b>:\n{desert_description}\n\n"
                         f"<b>Цена</b>: {desert_price}\n\n"
                         f"Для добавления в корзину нажмите на тэг справа :backhand_index_pointing_right: {desert_tag}"),
                         parse_mode="html")

    elif 'drinks' in call.data:
        number = int(str(call.data)[-1])

        drink_name = list(drink_name_tag.keys())[number - 1]
        drink_description = drink_name_description[drink_name]
        drink_price = drink_name_price[drink_name]
        drink_tag = drink_name_tag[drink_name]

        bot.send_message(call.message.chat.id,
                         emoji.emojize(f"<b>{drink_name}</b>"
                         f"\n\n<b>Описание</b>:\n{drink_description}\n\n"
                         f"<b>Цена</b>: {drink_price}\n\n"
                         f"Для добавления в корзину нажмите на тэг справа :backhand_index_pointing_right: {drink_tag}"),
                         parse_mode="html")


@bot.message_handler(content_types=['location'])
def location(message):
    if message.location is not None:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = types.KeyboardButton(text=emoji.emojize("Оплатить... :money_with_wings:"))
        button2 = types.KeyboardButton(text="Назад")

        keyboard.add(button)
        keyboard.add(button2)

        bot.send_message(message.from_user.id,
                         emoji.emojize('Отлично! Осталось только оплатить счёт, брат :star-struck:'),
                         reply_markup=keyboard)


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     emoji.emojize('От души, брат! :ok_hand: Заказывай ещё. Приятного аппетита :face_savoring_food:'),
                     parse_mode='Markdown', reply_markup=markup)


bot.polling(skip_pending=True)
