from telebot import types


# функция создания кнопок для клавиатуры
def reply_markup_maker(button_num: int, names_of_buttons: list, resized: bool):
    try:
        assert len(names_of_buttons) == button_num
        markup = types.ReplyKeyboardMarkup(resize_keyboard=resized)

        for i in range(button_num):
            markup.add(types.KeyboardButton(names_of_buttons[i]))

        return markup

    except AssertionError:
        print('Неверное количество имен или количество кнопок')


# функция создания кнопок для сообщений
def inline_markup_maker(button_num: int, names_of_buttons: list, callback_list: list, rows: int):
    try:
        assert len(names_of_buttons) == button_num
        assert len(names_of_buttons) == len(callback_list)
        markup = types.InlineKeyboardMarkup(row_width=rows)

        for i in range(button_num):
            markup.add(types.InlineKeyboardButton(names_of_buttons[i], callback_data=callback_list[i]))

        return markup

    except AssertionError:
        print('Неверно указаны параметры')


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
